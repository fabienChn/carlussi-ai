import * as dotenv from 'dotenv';
import * as readline from 'readline';
import { getConvoResponse } from './langchainUTILS';
import { TextLoader } from "langchain/document_loaders/fs/text";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";

dotenv.config();

type LoadedDocument = {
    pageContent: string;
    metadata: Record<string, any>;
};

const loader = new TextLoader(`${__dirname}/../dist/data.txt`);

// Create readline interface for interactive chat
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Initial conversation setup
const conversation = [
    { role: 'system', content: 'You are a helpful assistant.' }
];

// Define the chat loop
const chatLoop = (docs: LoadedDocument[]) => {
    rl.question("You: ", async (userInput) => {
        conversation.push({ role: 'user', content: userInput });
        
        // Extract the pageContent from each document
        const docsText = docs.map(doc => doc.pageContent);
        
        // Pass the extracted text data to getConvoResponse function
        const response = await getConvoResponse(userInput, docsText);
        
        console.log(`Assistant: ${response.response}`);
        chatLoop(docs); // Loop back for the next user input
    });
};

(async () => {
    const docs = await loader.load();

    // Load the docs into the vector store
    const vectorStore = await MemoryVectorStore.fromDocuments(
        docs,
        new OpenAIEmbeddings()
    );

    console.log(docs)
    // Start the chat loop
    chatLoop(docs);
})();
