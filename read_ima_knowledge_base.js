#!/usr/bin/env node
/**
 * Node.js 脚本 - 直接调用 IMA API 读取"经典V102"知识库的全部笔记内容
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// IMA API 配置
const IMA_API_BASE = 'https://ima.qq.com';
const IMA_CLIENT_ID = '910fce0cc27f5685b8f06c9d88a9ae1e';
const IMA_API_KEY = 'BrqdfQbt50sKsme7VZX0xeTR4qwEYjS+vxUJP/2wiG5S57RGo7JB9uCh290CcXZuu6g88F4U8A==';

/**
 * 调用 IMA OpenAPI
 */
function imaApiCall(path, body, module = 'wiki') {
    return new Promise((resolve, reject) => {
        const url = `${IMA_API_BASE}/openapi/${module}/v1/${path}`;
        
        const postData = JSON.stringify(body);
        
        const options = {
            method: 'POST',
            headers: {
                'ima-openapi-clientid': IMA_CLIENT_ID,
                'ima-openapi-apikey': IMA_API_KEY,
                'Content-Type': 'application/json; charset=utf-8',
                'Content-Length': Buffer.byteLength(postData)
            }
        };
        
        const req = https.request(url, options, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const result = JSON.parse(data);
                    resolve(result);
                } catch (e) {
                    resolve({
                        retcode: -1,
                        errmsg: `JSON parse error: ${e.message}`
                    });
                }
            });
        });
        
        req.on('error', (e) => {
            resolve({
                retcode: -1,
                errmsg: `${e.name}: ${e.message}`
            });
        });
        
        req.write(postData);
        req.end();
    });
}

/**
 * 搜索知识库
 */
async function searchKnowledgeBase(query, limit = 20) {
    console.log(`🔍 搜索知识库: query='${query}', limit=${limit}`);
    
    const body = {
        query: query,
        cursor: '',
        limit: limit
    };
    
    const response = await imaApiCall('search_knowledge_base', body);
    
    if (response.retcode === 0 || response.code === 0) {
        const data = response.data || response;
        const results = data.infos || [];
        console.log(`✅ 找到 ${results.length} 个知识库`);
        return results;
    } else {
        console.log(`❌ 搜索失败: ${response.errmsg || response.msg || 'Unknown error'}`);
        return [];
    }
}

/**
 * 获取知识库详情
 */
async function getKnowledgeBase(ids) {
    console.log(`📚 获取知识库详情: ids=${JSON.stringify(ids)}`);
    
    const body = {
        ids: ids
    };
    
    const response = await imaApiCall('get_knowledge_base', body);
    
    if (response.retcode === 0 || response.code === 0) {
        const data = response.data || response;
        const infos = data.infos || {};
        console.log(`✅ 获取到 ${Object.keys(infos).length} 个知识库详情`);
        return infos;
    } else {
        console.log(`❌ 获取详情失败: ${response.errmsg || response.msg || 'Unknown error'}`);
        return {};
    }
}

/**
 * 浏览知识库内容列表
 */
async function listKnowledge(kbId, folderId = '', limit = 50) {
    console.log(`📂 浏览知识库内容: kb_id=${kbId.substring(0, 20)}..., folder_id=${folderId}, limit=${limit}`);
    
    const body = {
        knowledge_base_id: kbId,
        cursor: '',
        limit: limit
    };
    
    if (folderId) {
        body.folder_id = folderId;
    }
    
    const response = await imaApiCall('get_knowledge_list', body);
    
    if (response.retcode === 0 || response.code === 0) {
        const data = response.data || response;
        const knowledgeList = data.knowledge_list || [];
        console.log(`✅ 找到 ${knowledgeList.length} 个内容`);
        return knowledgeList;
    } else {
        console.log(`❌ 浏览失败: ${response.errmsg || response.msg || 'Unknown error'}`);
        return [];
    }
}

/**
 * 获取笔记内容（完整流程）
 */
async function getNoteContent(kbId, docId, format = 'text') {
    // 步骤1: 调用 get_media_info 获取笔记的 notebook_id
    const mediaId = docId;
    
    const mediaInfoResponse = await imaApiCall('get_media_info', {
        knowledge_base_id: kbId,
        media_id: mediaId
    });
    
    if (mediaInfoResponse.retcode !== 0 && mediaInfoResponse.code !== 0) {
        return {
            status: 'error',
            message: `Failed to get media info: ${mediaInfoResponse.errmsg || mediaInfoResponse.msg || 'Unknown error'}`
        };
    }
    
    // 提取 notebook_id
    const data = mediaInfoResponse.data || mediaInfoResponse;
    const notebookExtInfo = data.note_book_ext_info || {};
    let notebookId = notebookExtInfo.note_book_id || '';
    
    if (!notebookId) {
        notebookId = data.note_book_id || data.note_id || '';
    }
    
    if (!notebookId) {
        return {
            status: 'error',
            message: 'This document does not appear to be a note (no notebook_id found)'
        };
    }
    
    // 步骤2: 调用 note/v1/get_doc_content 获取笔记内容
    const noteContent = await imaApiCall('get_doc_content', {
        note_id: notebookId,
        format: format
    }, 'note');
    
    if (noteContent.retcode !== 0 && noteContent.code !== 0) {
        return {
            status: 'error',
            message: `Failed to get doc content: ${noteContent.errmsg || noteContent.msg || 'Unknown error'}`
        };
    }
    
    const contentData = noteContent.data || noteContent;
    
    return {
        status: 'success',
        doc_id: docId,
        notebook_id: notebookId,
        content: contentData.content || '',
        title: contentData.title || ''
    };
}

/**
 * 主程序
 */
async function main() {
    console.log('='.repeat(60));
    console.log('IMA 知识库读取工具 - 经典V102');
    console.log('='.repeat(60));
    
    // 步骤1: 搜索"经典V102"知识库
    let kbList = await searchKnowledgeBase('经典V102', 20);
    
    if (!kbList || kbList.length === 0) {
        console.log('\n❌ 未找到"经典V102"知识库，尝试列出所有知识库...');
        kbList = await searchKnowledgeBase('', 50);
        
        if (!kbList || kbList.length === 0) {
            console.log('❌ 未找到任何知识库');
            process.exit(1);
        }
    }
    
    // 找到"经典V102"知识库
    let targetKb = null;
    for (const kb of kbList) {
        const kbName = kb.name || '';
        console.log(`  知识库: ${kbName} (ID: ${kb.id || ''})`);
        if (kbName.includes('经典V102') || kbName.includes('V102')) {
            targetKb = kb;
            break;
        }
    }
    
    if (!targetKb) {
        console.log(`\n⚠️ 未找到名称完全匹配的"经典V102"知识库，使用第一个: ${kbList[0].name || ''}`);
        targetKb = kbList[0];
    }
    
    const kbId = targetKb.id || '';
    const kbName = targetKb.name || '';
    console.log(`\n✅ 目标知识库: ${kbName} (ID: ${kbId})`);
    
    // 步骤2: 获取知识库详情
    const kbDetails = await getKnowledgeBase([kbId]);
    if (kbDetails[kbId]) {
        const kbDetail = kbDetails[kbId];
        console.log(`  名称: ${kbDetail.name || ''}`);
        console.log(`  描述: ${kbDetail.description || ''}`);
    }
    
    // 步骤3: 浏览知识库内容
    console.log('\n📂 浏览知识库内容...');
    const knowledgeList = await listKnowledge(kbId, '', 50);
    
    if (!knowledgeList || knowledgeList.length === 0) {
        console.log('❌ 知识库为空或读取失败');
        process.exit(1);
    }
    
    // 步骤4: 提取所有笔记
    const notes = [];
    const folders = [];
    
    for (const item of knowledgeList) {
        const itemType = item.type || 0;
        const itemName = item.title || item.name || '';
        const itemId = item.id || '';
        
        if (itemType === 11) {  // 笔记类型
            notes.push(item);
            console.log(`  📄 ${itemName} (ID: ${itemId.substring(0, 30)}...)`);
        } else if (itemType === 1) {  // 文件夹类型
            folders.push(item);
            console.log(`  📁 ${itemName} (ID: ${itemId.substring(0, 30)}...)`);
        } else {
            console.log(`  📄 ${itemName} (ID: ${itemId.substring(0, 30)}..., type=${itemType})`);
        }
    }
    
    console.log(`\n📊 统计: ${notes.length} 篇笔记, ${folders.length} 个文件夹`);
    
    // 步骤5: 读取所有笔记内容
    console.log('\n📖 读取所有笔记内容...');
    const notesContent = [];
    
    for (let i = 0; i < notes.length; i++) {
        const note = notes[i];
        const docId = note.id || '';
        const title = note.title || '';
        
        console.log(`  [${i + 1}/${notes.length}] 读取: ${title}...`);
        
        const contentResult = await getNoteContent(kbId, docId, 'text');
        
        if (contentResult.status === 'success') {
            console.log(`    ✅ (内容长度: ${contentResult.content.length})`);
            notesContent.push({
                title: title,
                doc_id: docId,
                notebook_id: contentResult.notebook_id,
                content: contentResult.content
            });
        } else {
            console.log(`    ❌ ${contentResult.message}`);
        }
        
        // 避免 API 限流
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 步骤6: 保存结果
    console.log('\n💾 保存结果...);
    
    const outputFile = 'ima_classic_v102_notes.json';
    const outputData = {
        knowledge_base: {
            id: kbId,
            name: kbName
        },
        notes_count: notesContent.length,
        notes: notesContent
    };
    
    fs.writeFileSync(outputFile, JSON.stringify(outputData, null, 2), 'utf8');
    console.log(`✅ 结果已保存到: ${outputFile}`);
    console.log(`   共 ${notesContent.length} 篇笔记`);
    
    // 也保存纯文本版本
    const txtFile = 'ima_classic_v102_notes.txt';
    let txtContent = `# IMA 知识库: ${kbName}\n\n`;
    txtContent += `知识库 ID: ${kbId}\n`;
    txtContent += `笔记数量: ${notesContent.length}\n`;
    txtContent += `导出时间: ${new Date().toLocaleString('zh-CN')}\n\n`;
    txtContent += '='.repeat(60) + '\n\n';
    
    for (let i = 0; i < notesContent.length; i++) {
        const note = notesContent[i];
        txtContent += `## ${i + 1}. ${note.title}\n\n`;
        txtContent += note.content;
        txtContent += '\n\n' + '='.repeat(60) + '\n\n';
    }
    
    fs.writeFileSync(txtFile, txtContent, 'utf8');
    console.log(`✅ 纯文本版本已保存到: ${txtFile}`);
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ 完成！');
    console.log('='.repeat(60));
}

main().catch(e => {
    console.error('❌ 错误:', e);
    process.exit(1);
});
