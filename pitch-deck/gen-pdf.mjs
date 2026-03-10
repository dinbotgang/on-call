import puppeteer from 'puppeteer';
import { resolve } from 'path';
import { pathToFileURL } from 'url';

const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 720 });

const slides = 9;
const { PDFDocument } = await import('pdf-lib');
const pdfDoc = await PDFDocument.create();

const url = pathToFileURL(resolve('index.html')).href;
await page.goto(url, { waitUntil: 'networkidle0' });

for (let i = 0; i < slides; i++) {
  if (i > 0) await page.evaluate(() => window.next());
  await new Promise(r => setTimeout(r, 300));
  const pdfBytes = await page.pdf({ width: '1280px', height: '720px', printBackground: true });
  const srcDoc = await PDFDocument.load(pdfBytes);
  const [pg] = await pdfDoc.copyPages(srcDoc, [0]);
  pdfDoc.addPage(pg);
}

await browser.close();
import { writeFileSync } from 'fs';
writeFileSync('pitch-deck.pdf', await pdfDoc.save());
console.log('Done');
