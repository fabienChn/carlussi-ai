import * as dotenv from 'dotenv';

dotenv.config();

// Updated imports from 'langchain'
import { OpenAI } from 'langchain/llms/openai';
import { ChatOpenAI } from 'langchain/chat_models/openai';
import { BufferMemory } from 'langchain/memory';
import { ConversationChain } from 'langchain/chains';
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const llm = new OpenAI({ openAIApiKey: OPENAI_API_KEY });
const chat = new ChatOpenAI({ temperature: 0, openAIApiKey: OPENAI_API_KEY });
const memory = new BufferMemory();
const chain = new ConversationChain({ llm, memory });

export const getPrediction = async (prompt: string) => await llm.predict(prompt);
export const getChatPrediction = async (message: string) => await chat.predict(message);
export const getConvoResponse = async (input: string, docs: string[]) => {
    // Split the user input into words
    // const inputWords = input.split(' ');

    // // Use 'docs' (your loaded data) to check if input matches any content in the docs
    // for (const doc of docs) {
    //     // Split the document content into words
    //     const docWords = doc.split(' ');

    //     // Check if the important words from the user input are included in the document
    //     if (inputWords.some(word => docWords.includes(word))) {
    //         return { response: `Based on the documents: ${doc}` };
    //     }
    // }
    
    // Load the docs into the vector store
    const vectorStore = await MemoryVectorStore.fromDocuments(
        docs,
        new OpenAIEmbeddings()
    );

    console.log(vectorStore)
 
    // If not found in docs, process with OpenAI chain
    return await chain.call({ input });
};