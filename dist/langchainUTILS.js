"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getConvoResponse = exports.getChatPrediction = exports.getPrediction = void 0;
const dotenv = __importStar(require("dotenv"));
dotenv.config();
const openai_1 = require("langchain/llms/openai");
const openai_2 = require("langchain/chat_models/openai");
const memory_1 = require("langchain/memory");
const chains_1 = require("langchain/chains");
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const llm = new openai_1.OpenAI({ openAIApiKey: OPENAI_API_KEY });
const chat = new openai_2.ChatOpenAI({ temperature: 0, openAIApiKey: OPENAI_API_KEY });
const memory = new memory_1.BufferMemory();
const chain = new chains_1.ConversationChain({ llm, memory });
const getPrediction = async (prompt) => await llm.predict(prompt);
exports.getPrediction = getPrediction;
const getChatPrediction = async (message) => await chat.predict(message);
exports.getChatPrediction = getChatPrediction;
const getConvoResponse = async (input, docs) => {
    const inputWords = input.split(' ');
    for (const doc of docs) {
        const docWords = doc.split(' ');
        if (inputWords.some(word => docWords.includes(word))) {
            return { response: `Based on the documents: ${doc}` };
        }
    }
    return await chain.call({ input });
};
exports.getConvoResponse = getConvoResponse;
