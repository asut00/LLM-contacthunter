from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
import os

def get_api_key():
    try:
        with open("github_token.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: github_token.txt file not found.")
        exit(1)

API_KEY = get_api_key()

# DATABASE

DATABASE_URL = "sqlite:///./contacts.db"
database = Database(DATABASE_URL)
Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# API

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import nest_asyncio
import json

from pdf2image import convert_from_bytes
import pytesseract
from openai import OpenAI

app = FastAPI(title="PDF-analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_contact_info(text):
	client = OpenAI(
		base_url="https://models.inference.ai.azure.com",
		api_key=API_KEY
	)
	response = client.chat.completions.create(
		messages=[
			{
				"role": "system",
				"content": "",
			},
			{
				"role": "user",
				"content": f"Identify the contact informations (the name, the address, the phone number and the email) in this text and return them in json format with the keys name, address, phone_number and email (Your response needs to contain only the data in raw json format, nothing else, no need for '\n', no need for ```json``` either) : {text}",
			},
		],
		model="gpt-4o-mini",
		temperature=1,
		max_tokens=4096,
		top_p=1,
	)
	return response.choices[0].message.content

def extract_text_from_bytes(pdf_bytes):
	images = convert_from_bytes(pdf_bytes)
	text = ""
	for image in images:
		text += pytesseract.image_to_string(image) + "\n"
	return text

@app.get("/")
def home():
	return("Welcome to the PDF analysis API!")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
	# check if file is a PDF
	if not file.filename.endswith(".pdf"):
		raise HTTPException(status_code=400, detail="Error: Invalid file type. Please upload a PDF.")
	try:
		# convert PDF to image
		pdf_bytes = await file.read()
		extracted_text = extract_text_from_bytes(pdf_bytes)
		contact_infos = extract_contact_info(extracted_text)
		parsed_contact_infos = json.loads(contact_infos)

		# store in db
		db = SessionLocal()
		contact_entry = Contact(
			name=parsed_contact_infos.get("name", None),
			address=parsed_contact_infos.get("address", None),
			phone=parsed_contact_infos.get("phone_number", None),
			email=parsed_contact_infos.get("email", None)
		)
		db.add(contact_entry)
		db.commit()
		db.refresh(contact_entry)
		db.close()

		return (parsed_contact_infos)
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/contacts")
async def get_contacts():
	db = SessionLocal()
	contacts = db.query(Contact).all()
	db.close()
	return contacts

nest_asyncio.apply()

host = "0.0.0.0"

uvicorn.run(app, host=host, port=8000)