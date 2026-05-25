/**
 * 灵助 SDK - C语言绑定实现（V185.0）
 * Lingzhu SDK - C Bindings Implementation
 * 
 * 实现缓存感知调度器、边缘推理适配器、三进制逻辑仿真的C接口
 */

#include "lingzhu_sdk.h"
#include <stdlib.h>
#include <string.h>
#include <time.h>

// ==================== 缓存调度器实现 ====================

/**
 * 缓存项结构
 */
typedef struct LingzhuCacheItem {
    char* key;
    char* value;
    size_t access_count;
    time_t last_access;
    struct LingzhuCacheItem* prev;
    struct LingzhuCacheItem* next;
} LingzhuCacheItem;

/**
 * 缓存调度器结构
 */
struct LingzhuCacheScheduler {
    size_t capacity;
    size_t size;
    LingzhuCachePolicy current_policy;
    LingzhuCacheItem** items;  // 哈希表
    LingzhuCacheItem* head;      // LRU链表头
    LingzhuCacheItem* tail;      // LRU链表尾
    size_t hit_count;
    size_t miss_count;
};

// 哈希函数
static size_t hash_key(const char* key, size_t capacity) {
    size_t hash = 0;
    while (*key) {
        hash = (hash * 31 + *key) % capacity;
        key++;
    }
    return hash;
}

// 创建缓存项
static LingzhuCacheItem* create_item(const char* key, const char* value) {
    LingzhuCacheItem* item = (LingzhuCacheItem*)malloc(sizeof(LingzhuCacheItem));
    if (!item) return NULL;
    
    item->key = (char*)malloc(strlen(key) + 1);
    item->value = value ? (char*)malloc(strlen(value) + 1) : NULL;
    
    if (item->key) strcpy(item->key, key);
    if (item->value && value) strcpy(item->value, value);
    
    item->access_count = 1;
    item->last_access = time(NULL);
    item->prev = item->next = NULL;
    
    return item;
}

// LRU链表操作
static void move_to_head(LingzhuCacheScheduler* scheduler, LingzhuCacheItem* item) {
    if (item == scheduler->head) return;
    
    // 从当前位置移除
    if (item->prev) item->prev->next = item->next;
    if (item->next) item->next->prev = item->prev;
    if (item == scheduler->tail) scheduler->tail = item->prev;
    
    // 移动到头部
    item->prev = NULL;
    item->next = scheduler->head;
    if (scheduler->head) scheduler->head->prev = item;
    scheduler->head = item;
    if (!scheduler->tail) scheduler->tail = item;
}

// ==================== API实现 ====================

LingzhuCacheScheduler* lingzhu_cache_create(size_t capacity) {
    LingzhuCacheScheduler* scheduler = (LingzhuCacheScheduler*)malloc(sizeof(LingzhuCacheScheduler));
    if (!scheduler) return NULL;
    
    scheduler->capacity = capacity;
    scheduler->size = 0;
    scheduler->current_policy = LINGZHU_CACHE_LRU;
    scheduler->hit_count = 0;
    scheduler->miss_count = 0;
    scheduler->head = scheduler->tail = NULL;
    
    scheduler->items = (LingzhuCacheItem**)calloc(capacity, sizeof(LingzhuCacheItem*));
    if (!scheduler->items) {
        free(scheduler);
        return NULL;
    }
    
    return scheduler;
}

void lingzhu_cache_destroy(LingzhuCacheScheduler* scheduler) {
    if (!scheduler) return;
    
    // 释放所有缓存项
    for (size_t i = 0; i < scheduler->capacity; i++) {
        LingzhuCacheItem* item = scheduler->items[i];
        while (item) {
            LingzhuCacheItem* next = item->next;
            free(item->key);
            free(item->value);
            free(item);
            item = next;
        }
    }
    
    free(scheduler->items);
    free(scheduler);
}

LingzhuError lingzhu_cache_access(LingzhuCacheScheduler* scheduler, 
                                   const char* key, 
                                   const char* value) {
    if (!scheduler || !key) return LINGZHU_ERROR_INVALID_ARG;
    
    size_t idx = hash_key(key, scheduler->capacity);
    LingzhuCacheItem* item = scheduler->items[idx];
    
    // 查找键
    while (item) {
        if (strcmp(item->key, key) == 0) {
            if (value) {
                // 写操作
                free(item->value);
                item->value = (char*)malloc(strlen(value) + 1);
                if (!item->value) return LINGZHU_ERROR_OUT_OF_MEMORY;
                strcpy(item->value, value);
            }
            
            item->access_count++;
            item->last_access = time(NULL);
            
            // LRU：移动到头部
            if (scheduler->current_policy == LINGZHU_CACHE_LRU) {
                move_to_head(scheduler, item);
            }
            
            scheduler->hit_count++;
            return LINGZHU_OK;
        }
        item = item->next;
    }
    
    // 未找到
    scheduler->miss_count++;
    
    if (!value) {
        // 读操作且未找到
        return LINGZHU_ERROR_NOT_FOUND;
    }
    
    // 写操作：创建新项
    if (scheduler->size >= scheduler->capacity) {
        // 需要淘汰
        // TODO: 根据策略淘汰
        // 简化：淘汰尾部
        if (scheduler->tail) {
            LingzhuCacheItem* to_remove = scheduler->tail;
            scheduler->tail = to_remove->prev;
            if (scheduler->tail) scheduler->tail->next = NULL;
            
            size_t remove_idx = hash_key(to_remove->key, scheduler->capacity);
            scheduler->items[remove_idx] = to_remove->next;
            
            free(to_remove->key);
            free(to_remove->value);
            free(to_remove);
            scheduler->size--;
        }
    }
    
    LingzhuCacheItem* new_item = create_item(key, value);
    if (!new_item) return LINGZHU_ERROR_OUT_OF_MEMORY;
    
    // 插入哈希表
    new_item->next = scheduler->items[idx];
    scheduler->items[idx] = new_item;
    
    // 插入LRU链表头部
    new_item->next = scheduler->head;
    if (scheduler->head) scheduler->head->prev = new_item;
    scheduler->head = new_item;
    if (!scheduler->tail) scheduler->tail = new_item;
    
    scheduler->size++;
    return LINGZHU_OK;
}

LingzhuError lingzhu_cache_switch_policy(LingzhuCacheScheduler* scheduler,
                                          LingzhuCachePolicy policy) {
    if (!scheduler) return LINGZHU_ERROR_INVALID_ARG;
    scheduler->current_policy = policy;
    return LINGZHU_OK;
}

LingzhuError lingzhu_cache_get_stats(LingzhuCacheScheduler* scheduler,
                                      size_t* hit_count,
                                      size_t* miss_count,
                                      LingzhuCachePolicy* current_policy) {
    if (!scheduler) return LINGZHU_ERROR_INVALID_ARG;
    
    if (hit_count) *hit_count = scheduler->hit_count;
    if (miss_count) *miss_count = scheduler->miss_count;
    if (current_policy) *current_policy = scheduler->current_policy;
    
    return LINGZHU_OK;
}

// ==================== 边缘推理适配器（占位实现）====================

struct LingzhuEdgeAdapter {
    LingzhuDeviceType device_type;
    size_t memory_mb;
    bool has_gpu;
};

LingzhuEdgeAdapter* lingzhu_edge_create() {
    LingzhuEdgeAdapter* adapter = (LingzhuEdgeAdapter*)malloc(sizeof(LingzhuEdgeAdapter));
    if (!adapter) return NULL;
    
    adapter->device_type = LINGZHU_DEVICE_CPU;
    adapter->memory_mb = 4096;  // 默认4GB
    adapter->has_gpu = false;
    
    return adapter;
}

void lingzhu_edge_destroy(LingzhuEdgeAdapter* adapter) {
    if (!adapter) return;
    free(adapter);
}

LingzhuError lingzhu_edge_detect_device(LingzhuEdgeAdapter* adapter,
                                         LingzhuDeviceType* device_type,
                                         size_t* memory_mb,
                                         bool* has_gpu) {
    if (!adapter) return LINGZHU_ERROR_INVALID_ARG;
    
    if (device_type) *device_type = adapter->device_type;
    if (memory_mb) *memory_mb = adapter->memory_mb;
    if (has_gpu) *has_gpu = adapter->has_gpu;
    
    return LINGZHU_OK;
}

LingzhuError lingzhu_edge_register_model(LingzhuEdgeAdapter* adapter,
                                          const char* model_name,
                                          float model_size_mb,
                                          float required_memory_gb) {
    if (!adapter || !model_name) return LINGZHU_ERROR_INVALID_ARG;
    // 占位实现
    return LINGZHU_OK;
}

LingzhuError lingzhu_edge_adapt_inference(LingzhuEdgeAdapter* adapter,
                                            const char* model_name,
                                            const char* input_json,
                                            char** output_json) {
    if (!adapter || !model_name || !output_json) return LINGZHU_ERROR_INVALID_ARG;
    // 占位实现
    *output_json = (char*)malloc(100);
    if (!*output_json) return LINGZHU_ERROR_OUT_OF_MEMORY;
    strcpy(*output_json, "{\"status\": \"not_implemented\"}");
    return LINGZHU_OK;
}

// ==================== 三进制逻辑实现 ====================

LingzhuTrit lingzhu_ternary_min(LingzhuTrit a, LingzhuTrit b) {
    if (a == LINGZHU_TRIT_YIN || b == LINGZHU_TRIT_YIN) return LINGZHU_TRIT_YIN;
    if (a == LINGZHU_TRIT_HE || b == LINGZHU_TRIT_HE) return LINGZHU_TRIT_HE;
    return LINGZHU_TRIT_YANG;  // a == b == YANG
}

LingzhuTrit lingzhu_ternary_max(LingzhuTrit a, LingzhuTrit b) {
    if (a == LINGZHU_TRIT_YANG || b == LINGZHU_TRIT_YANG) return LINGZHU_TRIT_YANG;
    if (a == LINGZHU_TRIT_HE || b == LINGZHU_TRIT_HE) return LINGZHU_TRIT_HE;
    return LINGZHU_TRIT_YIN;  // a == b == YIN
}

LingzhuTrit lingzhu_ternary_mid(LingzhuTrit a, LingzhuTrit b) {
    // 中值 = he
    (void)a; (void)b;  // 未使用参数
    return LINGZHU_TRIT_HE;
}

LingzhuTrit lingzhu_ternary_shift(LingzhuTrit a, int shift) {
    if (shift == 0) return a;
    if (shift < 0) {
        // 阴化
        return LINGZHU_TRIT_YIN;
    } else {
        // 阳化
        return LINGZHU_TRIT_YANG;
    }
}

// ==================== 卦象19683实现 ====================

void lingzhu_hexagram_init(LingzhuHexagram19683* hexagram) {
    if (!hexagram) return;
    for (int i = 0; i < LINGZHU_HEXAGRAM_LENGTH; i++) {
        hexagram->trits[i] = LINGZHU_TRIT_HE;
    }
}

void lingzhu_hexagram_randomize(LingzhuHexagram19683* hexagram) {
    if (!hexagram) return;
    srand(time(NULL));
    for (int i = 0; i < LINGZHU_HEXAGRAM_LENGTH; i++) {
        int r = rand() % 3;
        hexagram->trits[i] = (LingzhuTrit)(r - 1);  // -1, 0, +1
    }
}

LingzhuError lingzhu_hexagram_from_string(LingzhuHexagram19683* hexagram, 
                                           const char* str) {
    if (!hexagram || !str) return LINGZHU_ERROR_INVALID_ARG;
    
    size_t len = strlen(str);
    if (len != LINGZHU_HEXAGRAM_LENGTH) return LINGZHU_ERROR_INVALID_ARG;
    
    for (size_t i = 0; i < len; i++) {
        if (str[i] == '-') {
            hexagram->trits[i] = LINGZHU_TRIT_YIN;
        } else if (str[i] == '0') {
            hexagram->trits[i] = LINGZHU_TRIT_HE;
        } else if (str[i] == '+') {
            hexagram->trits[i] = LINGZHU_TRIT_YANG;
        } else {
            return LINGZHU_ERROR_INVALID_ARG;
        }
    }
    
    return LINGZHU_OK;
}

void lingzhu_hexagram_to_string(LingzhuHexagram19683* hexagram, char* str) {
    if (!hexagram || !str) return;
    
    for (int i = 0; i < LINGZHU_HEXAGRAM_LENGTH; i++) {
        if (hexagram->trits[i] == LINGZHU_TRIT_YIN) {
            str[i] = '-';
        } else if (hexagram->trits[i] == LINGZHU_TRIT_HE) {
            str[i] = '0';
        } else {
            str[i] = '+';
        }
    }
    str[LINGZHU_HEXAGRAM_LENGTH] = '\0';
}

double lingzhu_hexagram_pi_coordinate(LingzhuHexagram19683* hexagram) {
    if (!hexagram) return 0.0;
    
    // 简化：将9位三进制转换为数字，然后除以19683
    int value = 0;
    for (int i = 0; i < LINGZHU_HEXAGRAM_LENGTH; i++) {
        value = value * 3 + (hexagram->trits[i] + 1);  // -1,0,+1 -> 0,1,2
    }
    
    return (double)value / 19683.0 * 3.141592653589793;
}

uint64_t lingzhu_hexagram_e_timestamp(LingzhuHexagram19683* hexagram) {
    if (!hexagram) return 0;
    
    // 简化：使用当前时间戳
    return (uint64_t)time(NULL);
}

// ==================== 版本和错误处理 ====================

const char* lingzhu_get_version() {
    return LINGZHU_SDK_VERSION;
}

const char* lingzhu_get_error_string(LingzhuError error) {
    switch (error) {
        case LINGZHU_OK: return "成功";
        case LINGZHU_ERROR_INVALID_ARG: return "无效参数";
        case LINGZHU_ERROR_OUT_OF_MEMORY: return "内存不足";
        case LINGZHU_ERROR_IO: return "IO错误";
        case LINGZHU_ERROR_NOT_FOUND: return "未找到";
        case LINGZHU_ERROR_NOT_IMPLEMENTED: return "未实现";
        default: return "未知错误";
    }
}