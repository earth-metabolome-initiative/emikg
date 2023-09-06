-- Create the "translations" table to store translations.
-- The combination of the label and lang columns in the translations table
-- must be unique, so that we can have multiple translations for the same
-- label, but not multiple translations for the same label and lang.
CREATE TABLE translations (
    id SERIAL PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    lang VARCHAR(255) NOT NULL,
    translation TEXT NOT NULL,
    last_updated_by INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (label, lang)
);

-- Create the "users" table to store user information
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    -- Add other user-related fields as needed
);

-- Create the "tokens" table, which stores tokens for API access
-- for a given user without requiring the user to log in.
-- The table contains a token name, which when combined with the
-- user ID is unique. The token itself is a random string, generated
-- upon creation by the application.
-- Furthermore, the token itself must be unique, so that a user
-- can be identified uniquely by the token.
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    token_name VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    used_last_on TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, token_name)
    UNIQUE (token)
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

-- Create the "taxons" table to store metadata about taxons
CREATE TABLE taxons (
    id SERIAL PRIMARY KEY,
    taxon_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    -- Add other metadata fields as needed
    user_id INT REFERENCES users(id) ON DELETE CASCADE
    -- The taxon name must be unique
    UNIQUE (taxon_name)
);

-- Create the "samples" table to store sample information
CREATE TABLE samples (
    id SERIAL PRIMARY KEY,
    -- The name of the sample, which should be unique
    sample_name VARCHAR(255) NOT NULL,
    -- Some samples are derived from other samples,
    -- except for the first sample, which is not
    -- derived from any other sample. This means
    -- that the "derived_from" column can be NULL.
    derived_from INT REFERENCES samples(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    -- Add other sample-related fields as needed
    user_id INT REFERENCES users(id) ON DELETE CASCADE
    taxon_id INT REFERENCES taxons(id) ON DELETE CASCADE
    -- We require for the sample name to be unique
    UNIQUE (sample_name)
);

-- Create an index on the "user_id" column for faster queries
CREATE INDEX idx_user_id ON taxons (user_id);