const fs = require('fs');
const { PDFDocument } = require('pdf-lib');
const pdfjsLib = require('pdfjs-dist');

async function getPdfMetaAndFields(pdfPath) {
  const data = new Uint8Array(fs.readFileSync(pdfPath));
  const loadingTask = pdfjsLib.getDocument(data).promise;
  const pdf = await loadingTask.promise;

  // 获取元数据
  const meta = await pdf.getMetadata();
  console.log('元数据:', meta.info);

  // 获取表单字段名（通过遍历注释）
  let fieldNames = [];
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const annotations = await page.getAnnotations();
    annotations.forEach(ann => {
      if (ann.fieldName) {
        fieldNames.push(ann.fieldName);
      }
    });
  }
  console.log('表单字段名:', fieldNames);

  return { meta: meta.info, fieldNames };
}

async function modifyPdfForm(inputPath, outputPath, fieldValues) {
  // 读取PDF文件
  const existingPdfBytes = fs.readFileSync(inputPath);

  // 加载PDF
  const pdfDoc = await PDFDocument.load(existingPdfBytes);

  // 获取表单
  const form = pdfDoc.getForm();

  // 获取所有文本框名字
  const fields = form.getFields();
  console.log('PDF中的文本框名字:');
  fields.forEach(field => {
    const name = field.getName();
    console.log(name);
  });

  // 根据传入的fieldValues修改文本框内容
  for (const field of fields) {
    const name = field.getName();
    if (fieldValues[name] !== undefined) {
      try {
        field.setText(fieldValues[name]);
      } catch (e) {
        // 不是文本框类型会报错，忽略
      }
    }
  }

  // 保存修改后的PDF
  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync(outputPath, pdfBytes);
}

// 示例用法
const inputPdf = 'payroll.pdf'; // 你的原始PDF路径
const outputPdf = 'output.pdf'; // 修改后的PDF保存路径

// 你要填充的内容，key是文本框名字，value是要填的内容
const fieldValues = {
  'NameField': '张三',
  'AgeField': '28',
  // 其他字段...
};

modifyPdfForm(inputPdf, outputPdf, fieldValues)
  .then(() => console.log('PDF表单已修改并保存为output.pdf'))
  .catch(console.error);

// 用法
getPdfMetaAndFields('payroll.pdf');