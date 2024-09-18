#!/usr/bin/env python3

import json
import os
import subprocess
import tempfile
import argparse

def load_notes(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

def save_notes(filename, notes_dict):
    with open(filename, 'w') as file:
        json.dump(notes_dict, file, indent=4)

def add_note():
    topic = input("Enter the name of the topic: ").strip().lower()
    subtopic = input("Enter the name of the subtopic: ").strip().lower()
    
    if topic in notes_dict and subtopic in notes_dict[topic]:
        print("Existing notes found for this subtopic. Opening in editor...")
        notes = notes_dict[topic][subtopic]
    else:
        notes = []

    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.txt') as temp_file:
        temp_filename = temp_file.name
        temp_file.write('\n'.join(notes))
        temp_file.flush()
        temp_file.close()

        subprocess.run(['gedit', temp_filename])

        with open(temp_filename, 'r') as temp_file:
            edited_notes = temp_file.read().strip().split('\n')

    os.remove(temp_filename)

    return topic, subtopic, edited_notes

def search_notes(notes_dict):
    search_term = input("Enter the term to search: ").strip().lower()
    for topic, subtopics in notes_dict.items():
        for subtopic, notes in subtopics.items():
            if search_term in topic or search_term in subtopic or any(search_term in note for note in notes):
                print(f"Topic: {topic.capitalize()} - Subtopic: {subtopic.capitalize()}")
                for i, note in enumerate(notes, 1):
                    print(f" {i}. {note}")

def list_topics(notes_dict):
    if notes_dict:
        print("Topics to discuss:")
        for topic, subtopics in notes_dict.items():
            for subtopic in subtopics.keys():
                print(f" - {topic.capitalize()} - {subtopic.capitalize()}")
    else:
        print("No topics available.")

def display_full_note():
    topic = input("Enter the topic name: ").strip().lower()
    subtopic = input("Enter the subtopic name: ").strip().lower()
    if topic in notes_dict and subtopic in notes_dict[topic]:
        print(f"Full notes for topic '{topic.capitalize()}' - subtopic '{subtopic.capitalize()}':")
        for i, note in enumerate(notes_dict[topic][subtopic], 1):
            print(f"{i}. {note}")
    else:
        print("Topic or subtopic not found.")

def delete_note():
    topic = input("Enter the topic name: ").strip().lower()
    subtopic = input("Enter the subtopic name: ").strip().lower()
    if topic in notes_dict and subtopic in notes_dict[topic]:
        del notes_dict[topic][subtopic]
        if not notes_dict[topic]:
            del notes_dict[topic]
        print(f"Deleted notes for topic '{topic.capitalize()}' - subtopic '{subtopic.capitalize()}'.")
    else:
        print("Topic or subtopic not found.")

def main():
    global notes_dict
    home_dir = os.path.expanduser("~")
    
    filename = os.path.join(home_dir, 'notes.json')
    notes_dict = load_notes(filename)

    parser = argparse.ArgumentParser(description="Notes app")
    parser.add_argument('-e', '--edit', action='store_true', help="Add or edit a note")
    parser.add_argument('-f', '--search', action='store_true', help="Search notes")
    parser.add_argument('-l', '--list', action='store_true', help="List all topics")
    parser.add_argument('-s', '--show', action='store_true', help="Display full note")
    parser.add_argument('-d', '--delete', action='store_true', help="Delete a note")
    args = parser.parse_args()

    if args.edit:
        topic, subtopic, notes = add_note()
        if topic not in notes_dict:
            notes_dict[topic] = {}
        notes_dict[topic][subtopic] = notes
        save_notes(filename, notes_dict)
    elif args.search:
        search_notes(notes_dict)
    elif args.list:
        list_topics(notes_dict)
    elif args.show:
        display_full_note()
    elif args.delete:
        delete_note()
        save_notes(filename, notes_dict)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

# To run this script in Linux:
# 1. Open a terminal.
# 2. Navigate to the directory containing the script: cd /c:/Users/Tom/Desktop/Notes\ app/
# 3. Make the script executable: chmod +x main.py
# 4. Run the script with the desired command:
#    - Display help: ./main.py -h
#    - Add or edit a note: ./main.py -e
#    - Search notes: ./main.py -f
#    - List all topics: ./main.py -l
#    - Display full note: ./main.py -s
#    - Delete a note: ./main.py -d
