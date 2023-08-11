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
exports.get = exports.set = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const databasePath = path.join(__dirname, 'data.json');
if (!fs.existsSync(databasePath)) {
    fs.writeFileSync(databasePath, JSON.stringify({}));
}
const set = (key, value) => {
    const data = JSON.parse(fs.readFileSync(databasePath, 'utf-8'));
    data[key] = value;
    fs.writeFileSync(databasePath, JSON.stringify(data, null, 2));
};
exports.set = set;
const get = (key) => {
    const data = JSON.parse(fs.readFileSync(databasePath, 'utf-8'));
    return data[key];
};
exports.get = get;
