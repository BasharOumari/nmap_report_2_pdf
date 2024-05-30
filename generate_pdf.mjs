import fs from 'fs';
import markdownpdf from 'markdown-pdf';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

if (process.argv.length !== 4) {
    console.log("Usage: node generate_pdf.mjs <markdown_file> <output_file>");
    process.exit(1);
}

const markdownFile = process.argv[2];
const pdfOutputFile = process.argv[3];

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Ensure the output directory exists
const outputDir = path.dirname(path.resolve(pdfOutputFile));
if (outputDir) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// Debugging: print the paths
console.log(`Markdown path: ${path.resolve(markdownFile)}`);
console.log(`PDF path: ${path.resolve(pdfOutputFile)}`);

// Convert markdown to PDF with custom CSS
markdownpdf({
    cssPath: path.join(__dirname, 'style.css'),
    paperBorder: '20mm',
}).from(markdownFile).to(pdfOutputFile, function () {
    console.log(`PDF file generated: ${pdfOutputFile}`);
});
