const { spawn, exec } = require('child_process');
const path = require('path');
const fs = require('fs').promises;
const os = require('os');

class ODGProcessor {
    constructor(options = {}) {
        this.libreOfficePath = options.libreOfficePath || this.getDefaultLibreOfficePath();
        this.pythonPath = options.pythonPath || 'python';
        this.scriptPath = path.join(__dirname, 'python', 'odg_bridge.py');
    }

    /**
     * 获取默认的LibreOffice路径
     */
    getDefaultLibreOfficePath() {
        const platform = os.platform();
        if (platform === 'win32') {
            return 'C:\\Program Files\\LibreOffice\\program\\python.exe';
        } else if (platform === 'darwin') {
            return '/Applications/LibreOffice.app/Contents/MacOS/python';
        } else {
            return '/usr/lib/libreoffice/program/python3';
        }
    }

    /**
     * 执行Python脚本
     */
    async executePythonScript(command, args = []) {
        return new Promise((resolve, reject) => {
            const pythonArgs = [this.scriptPath, command, ...args];
            const pythonProcess = spawn(this.libreOfficePath, pythonArgs, {
                stdio: ['pipe', 'pipe', 'pipe']
            });

            let stdout = '';
            let stderr = '';

            pythonProcess.stdout.on('data', (data) => {
                stdout += data.toString();
            });

            pythonProcess.stderr.on('data', (data) => {
                stderr += data.toString();
            });

            pythonProcess.on('close', (code) => {
                if (code === 0) {
                    try {
                        // 先尝试直接解析为JSON
                        const result = JSON.parse(stdout);
                        resolve(result);
                    } catch (e) {
                        // 如果失败，尝试从stdout中提取JSON
                        try {
                            const lines = stdout.split('\n');
                            const jsonStart = lines.findIndex(line => line.trim().startsWith('{'));
                            if (jsonStart !== -1) {
                                const jsonStr = lines.slice(jsonStart).join('\n');
                                const result = JSON.parse(jsonStr);
                                resolve(result);
                            } else {
                                resolve({ success: true, output: stdout });
                            }
                        } catch (e2) {
                            resolve({ success: true, output: stdout });
                        }
                    }
                } else {
                    reject(new Error(`Python script failed with code ${code}: ${stderr}`));
                }
            });

            pythonProcess.on('error', (error) => {
                reject(new Error(`Failed to start Python process: ${error.message}`));
            });
        });
    }

    /**
     * 获取ODG文件信息
     * @param {string} filePath - ODG文件路径
     * @returns {Promise<Object>} 文件信息
     */
    async getODGInfo(filePath) {
        try {
            const absolutePath = path.resolve(filePath);
            const result = await this.executePythonScript('get_info', [absolutePath]);
            return result;
        } catch (error) {
            throw new Error(`Failed to get ODG info: ${error.message}`);
        }
    }

    /**
     * 批量修改ODG文件中的文本内容
     * @param {string} filePath - ODG文件路径
     * @param {Object} shapeTextMap - 形状名称到新文本的映射
     * @param {string} outputPath - 输出文件路径（可选）
     * @param {boolean} exportPDF - 是否导出PDF（默认true）
     * @returns {Promise<Object>} 修改结果
     */
    async modifyTexts(filePath, shapeTextMap, outputPath = null, exportPDF = true) {
        try {
            const absolutePath = path.resolve(filePath);
            const absoluteOutputPath = outputPath ? path.resolve(outputPath) : null;
            
            const args = [
                absolutePath,
                JSON.stringify(shapeTextMap),
                absoluteOutputPath || '',
                exportPDF.toString()
            ];

            const result = await this.executePythonScript('modify_texts', args);
            return result;
        } catch (error) {
            throw new Error(`Failed to modify texts: ${error.message}`);
        }
    }

    /**
     * 修改单个形状的文本内容
     * @param {string} filePath - ODG文件路径
     * @param {string} shapeName - 形状名称
     * @param {string} newText - 新文本内容
     * @param {string} outputPath - 输出文件路径（可选）
     * @param {boolean} exportPDF - 是否导出PDF（默认true）
     * @returns {Promise<Object>} 修改结果
     */
    async modifyText(filePath, shapeName, newText, outputPath = null, exportPDF = true) {
        const shapeTextMap = { [shapeName]: newText };
        return this.modifyTexts(filePath, shapeTextMap, outputPath, exportPDF);
    }

    /**
     * 创建新的ODG文件
     * @param {string} outputPath - 输出文件路径
     * @returns {Promise<Object>} 创建结果
     */
    async createODG(outputPath) {
        try {
            const absoluteOutputPath = path.resolve(outputPath);
            const result = await this.executePythonScript('create_odg', [absoluteOutputPath]);
            return result;
        } catch (error) {
            throw new Error(`Failed to create ODG: ${error.message}`);
        }
    }

    /**
     * 导出ODG为PDF
     * @param {string} filePath - ODG文件路径
     * @param {string} outputPath - PDF输出路径
     * @returns {Promise<Object>} 导出结果
     */
    async exportToPDF(filePath, outputPath) {
        try {
            const absolutePath = path.resolve(filePath);
            const absoluteOutputPath = path.resolve(outputPath);
            
            const result = await this.executePythonScript('export_pdf', [absolutePath, absoluteOutputPath]);
            return result;
        } catch (error) {
            throw new Error(`Failed to export PDF: ${error.message}`);
        }
    }
}

// 便捷函数
/**
 * 获取ODG文件信息
 * @param {string} filePath - ODG文件路径
 * @param {Object} options - 选项
 * @returns {Promise<Object>} 文件信息
 */
async function getODGInfo(filePath, options = {}) {
    const processor = new ODGProcessor(options);
    return processor.getODGInfo(filePath);
}

/**
 * 批量修改ODG文件文本
 * @param {string} filePath - ODG文件路径
 * @param {Object} shapeTextMap - 形状文本映射
 * @param {Object} options - 选项
 * @returns {Promise<Object>} 修改结果
 */
async function modifyODGTexts(filePath, shapeTextMap, options = {}) {
    const processor = new ODGProcessor(options);
    return processor.modifyTexts(
        filePath, 
        shapeTextMap, 
        options.outputPath, 
        options.exportPDF !== false
    );
}

/**
 * 修改单个ODG文件文本
 * @param {string} filePath - ODG文件路径
 * @param {string} shapeName - 形状名称
 * @param {string} newText - 新文本
 * @param {Object} options - 选项
 * @returns {Promise<Object>} 修改结果
 */
async function modifyODGText(filePath, shapeName, newText, options = {}) {
    const processor = new ODGProcessor(options);
    return processor.modifyText(
        filePath, 
        shapeName, 
        newText, 
        options.outputPath, 
        options.exportPDF !== false
    );
}

module.exports = {
    ODGProcessor,
    getODGInfo,
    modifyODGTexts,
    modifyODGText
}; 