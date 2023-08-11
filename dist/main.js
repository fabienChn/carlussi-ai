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
const dotenv = __importStar(require("dotenv"));
const readline = __importStar(require("readline"));
const langchainUTILS_1 = require("./langchainUTILS");
const text_1 = require("langchain/document_loaders/fs/text");
dotenv.config();
const loader = new text_1.TextLoader(`${__dirname}/../dist/data.txt`);
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
const conversation = [
    { role: 'system', content: 'You are a helpful assistant.' }
];
const chatLoop = (docs) => {
    rl.question("You: ", async (userInput) => {
        conversation.push({ role: 'user', content: userInput });
        const docsText = docs.map(doc => doc.pageContent);
        const response = await (0, langchainUTILS_1.getConvoResponse)(userInput, docsText);
        console.log(`Assistant: ${response.response}`);
        chatLoop(docs);
    });
};
(async () => {
    const docs = await loader.load();
    console.log(docs);
    chatLoop(docs);
})();
