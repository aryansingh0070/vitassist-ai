# VITAssist AI

VITAssist AI is a Retrieval-Augmented Generation (RAG) chatbot built using React, FastAPI, ChromaDB, and Google's Gemini API.

## Features

* Ask questions from VIT academic documents
* PDF ingestion and chunking
* Vector search using ChromaDB
* Gemini-powered answer generation
* React frontend
* FastAPI backend

## Tech Stack

* React + Vite
* FastAPI
* ChromaDB
* Gemini API
* Python

## Run Locally

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```
