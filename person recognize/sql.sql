DROP TABLE IF EXISTS person;

-- 1. Create the table with all necessary columns
CREATE TABLE persons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age VARCHAR(20),
    gender VARCHAR(20),
    phone VARCHAR(20),
    address TEXT,
    email VARCHAR(100),
    occupation VARCHAR(100),
    image_path TEXT, -- Storing just the filename (e.g., 'rajesh.jpg')
    embedding FLOAT8[] -- Used by DeepFace for recognition
);

-- 2. Insert sample data
-- NOTE: image_path is updated to just the filename to work with your new Flask route
INSERT INTO persons 
(name, age, gender, phone, address, email, occupation, image_path)
VALUES
(
    'Rajesh Shakya',
    '22',
    'Male',
    '9876543210',
    'Lucknow',
    'rajesh@gmail.com',
    'Student',
    'C:\Users\shaky\OneDrive\Desktop\person recognize\known_faces\rajesh.jpg'
),
(
    'Amit Kumar',
    '24',
    'Male',
    '9999999999',
    'Delhi',
    'amit@gmail.com',
    'Engineer',
    'C:\Users\shaky\OneDrive\Desktop\person recognize\known_faces\amit.jpg'
);

-- 3. Verify the data
SELECT * FROM persons;
