def read_file(filepath = r"C:\Users\Himanshi\OneDrive\Desktop\rtl chatbot\vlsi_notes.txt"):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text
def split_into_chunks(text, chunk_size=300):
    words = text.split()
    chunks = []
    current_chunk = []
    word_count = 0

    for word in words:
        current_chunk.append(word)
        word_count += 1

        if word_count >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            word_count = 0

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def main():
    filepath = r"C:\Users\Himanshi\OneDrive\Desktop\rtl chatbot\vlsi_notes.txt"

    print(f"Reading file: {filepath}")
    text = read_file(filepath)
    print(f"Total words in file: {len(text.split())}")
    print("-" * 50)

    chunks = split_into_chunks(text, chunk_size=300)
    print(f"Total chunks created: {len(chunks)}")
    print("=" * 50)

    for i, chunk in enumerate(chunks):
        print(f"\n--- CHUNK {i+1} ---")
        print(chunk)
        print(f"(Words in this chunk: {len(chunk.split())})")


if __name__ == '__main__':
    main()