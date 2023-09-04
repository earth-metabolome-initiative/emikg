-- Create the "translations" table to store translations
CREATE TABLE translations (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) NOT NULL UNIQUE,
    lang VARCHAR(10) NOT NULL,
    text TEXT NOT NULL
);

-- Create the "users" table to store user information
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    -- Add other user-related fields as needed
);

-- Create the "administrators" table to store administrator information
CREATE TABLE administrators (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    -- Add other administrator-related fields as needed
);

-- Create the "moderators" table to store moderator information
CREATE TABLE moderators (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    -- Add other moderator-related fields as needed
);

-- Create the "oauth_connections" table to store OAuth provider connections
CREATE TABLE oauth_connections (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    oauth_provider VARCHAR(255) NOT NULL,
    oauth_user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    -- Add other OAuth-related fields as needed
);

-- Create the "taxon" table to store metadata about taxon
CREATE TABLE taxon (
    id SERIAL PRIMARY KEY,
    taxon_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    -- Add other metadata fields as needed
    user_id INT REFERENCES users(id) ON DELETE CASCADE
);

-- Create the "samples" table to store sample information
CREATE TABLE samples (
    id SERIAL PRIMARY KEY,
    sample_name VARCHAR(255) NOT NULL,
    -- Some samples are derived from other samples,
    -- except for the first sample, which is not
    -- derived from any other sample
    derived_from INT REFERENCES samples(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    -- Add other sample-related fields as needed
    user_id INT REFERENCES users(id) ON DELETE CASCADE
);

-- Create an index on the "user_id" column for faster queries
CREATE INDEX idx_user_id ON species (user_id);