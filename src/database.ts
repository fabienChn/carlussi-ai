import * as fs from 'fs';
import * as path from 'path';

const databasePath = path.join(__dirname, 'data.json');

// Initialize the database if it doesn't exist
if (!fs.existsSync(databasePath)) {
    fs.writeFileSync(databasePath, JSON.stringify({}));
}

const set = (key: string, value: any) => {
    const data = JSON.parse(fs.readFileSync(databasePath, 'utf-8'));
    data[key] = value;
    fs.writeFileSync(databasePath, JSON.stringify(data, null, 2));
};

const get = (key: string) => {
    const data = JSON.parse(fs.readFileSync(databasePath, 'utf-8'));
    return data[key];
};

export { set, get };
