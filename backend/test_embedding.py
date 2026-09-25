from services.embedding import create_embedding

print("Test started")

text = "Customers can request a refund within 30 days."

embedding = create_embedding(text)

print("Embedding created")
print("Embedding length:", len(embedding))
print("First 5 values:", embedding[:5])