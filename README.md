# SHL Assessment Recommendation Chatbot

## Overview

This project is a FastAPI-based conversational recommendation system for SHL assessments.

Features:
- Semantic search using Sentence Transformers + FAISS
- Mistral AI powered conversational responses
- Clarifying questions
- Conversation history
- Off-topic guardrails

## Architecture

SHL Catalog
        ↓
Scraper
        ↓
catalog_clean.json
        ↓
Sentence Transformers
        ↓
FAISS
        ↓
FastAPI
        ↓
Mistral AI
        ↓
Recommendations

## Installation

pip install -r requirements.txt

## Run

uvicorn app.main:app --reload

## API

GET /health

POST /chat

## Example Request

{ ... }

## Technologies

- FastAPI
- Sentence Transformers
- FAISS
- Mistral AI
- BeautifulSoup