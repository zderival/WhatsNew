CREATE TABLE user_prefrences(id UUID PRIMARY KEY, user_id UUID REFERENCES "user"(id), topic TEXT);
CREATE TABLE saved_article( id UUID PRIMARY KEY, user_id UUID REFERENCES "user"(id), title TEXT, source TEXT, url TEXT, UNIQUE (user_id,url));
CREATE TABLE read_articles(id UUID PRIMARY KEY, user_id UUID REFERENCES "user"(id), source TEXT, url TEXT, read_at TIMESTAMP);
CREATE TABLE search_history(id UUID PRIMARY KEY, user_id UUID REFERENCES "user"(id), keyword TEXT, searched_at TIMESTAMP);
