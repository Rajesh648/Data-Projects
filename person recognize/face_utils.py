from deepface import DeepFace
import numpy as np
import os



from database import get_all_persons

# GENERATE FACE FINGERPRINT

def get_fingerprint(image_path):

    try:

        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            return None

        results = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet512", 
            enforce_detection=False,
            detector_backend="opencv"      
        )

        embedding = results[0]["embedding"]

        return np.array(embedding, dtype=np.float32)

    except Exception as e:

        print(f"Fingerprint Error: {e}")

        return None


# RECOGNIZE PERSON

def recognize_person(image_to_scan):

    current_fingerprint = get_fingerprint(image_to_scan)

    unknown_response = {

        "status": "UNKNOWN PERSON",

        "message": "Face not matched with database",

        "name": "Unknown",

        "similarity": "0%",

        "age": "-",

        "gender": "-",

        "phone": "-",

        "address": "-",

        "email": "-",

        "occupation": "-",

        "image": "/static/images/unknown.png"
    }

    if current_fingerprint is None:

        return unknown_response

    persons = get_all_persons()

    best_match = None

    highest_similarity = 0

    for p in persons:

        db_embedding = p[9]

        if db_embedding is None:
            continue

        try:

            db_embedding = np.array(
                db_embedding,
                dtype=np.float32
            )

            similarity = np.dot(
                current_fingerprint,
                db_embedding
            ) / (
                np.linalg.norm(current_fingerprint)
                * np.linalg.norm(db_embedding)
            )

            similarity_percent = round(
                similarity * 100,
                2
            )

            print(f"{p[1]} Similarity: {similarity_percent}%")

            if similarity_percent > highest_similarity:

                highest_similarity = similarity_percent

                best_match = p

        except Exception as e:

            print(f"Comparison Error: {e}")

    print(f"Highest Similarity: {highest_similarity}%")

    # UNKNOWN

    if highest_similarity < 30:

        return unknown_response

    # SIMILAR PERSON

    elif highest_similarity < 75:

        return {

            "status": "SIMILAR PERSON",

            "message": f"This face is similar to {best_match[1]}",

            "name": best_match[1],

            "similarity": f"{highest_similarity}%",

            "age": best_match[2],

            "gender": best_match[3],

            "phone": best_match[4],

            "address": best_match[5],

            "email": best_match[6],

            "occupation": best_match[7],

            "image": f"/get_db_image/{os.path.basename(best_match[8])}"
        }

    # VERIFIED

    else:

        return {

            "status": "PERSON VERIFIED",

            "message": f"This person matched with database person {best_match[1]}",

            "name": best_match[1],

            "similarity": f"{highest_similarity}%",

            "age": best_match[2],

            "gender": best_match[3],

            "phone": best_match[4],

            "address": best_match[5],

            "email": best_match[6],

            "occupation": best_match[7],

            "image": f"/get_db_image/{os.path.basename(best_match[8])}"
        }