/**
 * 灵助 SDK - C语言绑定（V185.0）
 * Lingzhu SDK - C Bindings
 * 
 * 提供缓存感知调度器、边缘推理适配器、三进制逻辑仿真的C接口
 */

#ifndef LINGZHU_SDK_H
#define LINGZHU_SDK_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// ==================== 版本信息 ====================
#define LINGZHU_SDK_VERSION "V185.0"
#define LINGZHU_SDK_MAJOR 185
#define LINGZHU_SDK_MINOR 0

// ==================== 错误码 ====================
typedef enum {
    LINGZHU_OK = 0,
    LINGZHU_ERROR_INVALID_ARG = -1,
    LINGZHU_ERROR_OUT_OF_MEMORY = -2,
    LINGZHU_ERROR_IO = -3,
    LINGZHU_ERROR_NOT_FOUND = -4,
    LINGZHU_ERROR_NOT_IMPLEMENTED = -99
} LingzhuError;

// ==================== 缓存策略 ====================
typedef enum {
    LINGZHU_CACHE_LRU = 0,      // 最近最少使用
    LINGZHU_CACHE_LFU = 1,      // 最不经常使用
    LINGZHU_CACHE_FIFO = 2,     // 先进先出
    LINGZHU_CACHE_CLOCK = 3,    // 时钟算法
    LINGZHU_CACHE_RANDOM = 4    // 随机替换
} LingzhuCachePolicy;

// ==================== 设备类型 ====================
typedef enum {
    LINGZHU_DEVICE_CPU = 0,      // CPU
    LINGZHU_DEVICE_GPU = 1,      // GPU
    LINGZHU_DEVICE_NPU = 2,      // NPU
    LINGZHU_DEVICE_MOBILE = 3,   // 移动设备
    LINGZHU_DEVICE_EMBEDDED = 4  // 嵌入式设备
} LingzhuDeviceType;

// ==================== 三进制（Trit） ====================
typedef enum {
    LINGZHU_TRIT_YIN = -1,  // 阴（-1）
    LINGZHU_TRIT_HE = 0,     // 和（0）
    LINGZHU_TRIT_YANG = 1    // 阳（+1）
} LingzhuTrit;

// ==================== 缓存调度器句柄 ====================
typedef struct LingzhuCacheScheduler LingzhuCacheScheduler;

/**
 * 创建缓存调度器
 * 
 * @param capacity 缓存容量
 * @return 调度器句柄，失败返回NULL
 */
LingzhuCacheScheduler* lingzhu_cache_create(size_t capacity);

/**
 * 销毁缓存调度器
 * 
 * @param scheduler 调度器句柄
 */
void lingzhu_cache_destroy(LingzhuCacheScheduler* scheduler);

/**
 * 访问缓存
 * 
 * @param scheduler 调度器句柄
 * @param key 键
 * @param value 值（如果为NULL则为读操作）
 * @return 成功返回LINGZHU_OK，失败返回错误码
 */
LingzhuError lingzhu_cache_access(LingzhuCacheScheduler* scheduler, 
                                   const char* key, 
                                   const char* value);

/**
 * 切换缓存策略
 * 
 * @param scheduler 调度器句柄
 * @param policy 新策略
 * @return 成功返回LINGZHU_OK，失败返回错误码
 */
LingzhuError lingzhu_cache_switch_policy(LingzhuCacheScheduler* scheduler,
                                          LingzhuCachePolicy policy);

/**
 * 获取缓存统计信息
 * 
 * @param scheduler 调度器句柄
 * @param hit_count 命中次数（输出）
 * @param miss_count 未命中次数（输出）
 * @param current_policy 当前策略（输出）
 * @return 成功返回LINGZHU_OK，失败返回错误码
 */
LingzhuError lingzhu_cache_get_stats(LingzhuCacheScheduler* scheduler,
                                      size_t* hit_count,
                                      size_t* miss_count,
                                      LingzhuCachePolicy* current_policy);

// ==================== 边缘推理适配器句柄 ====================
typedef struct LingzhuEdgeAdapter LingzhuEdgeAdapter;

/**
 * 创建边缘推理适配器
 * 
 * @return 适配器句柄，失败返回NULL
 */
LingzhuEdgeAdapter* lingzhu_edge_create();

/**
 * 销毁边缘推理适配器
 * 
 * @param adapter 适配器句柄
 */
void lingzhu_edge_destroy(LingzhuEdgeAdapter* adapter);

/**
 * 检测设备能力
 * 
 * @param adapter 适配器句柄
 * @param device_type 设备类型（输出）
 * @param memory_mb 可用内存（MB）（输出）
 * @param has_gpu 是否有GPU（输出）
 * @return 成功返回LINGZHU_OK，失败返回错误码
 */
LingzhuError lingzhu_edge_detect_device(LingzhuEdgeAdapter* adapter,
                                         LingzhuDeviceType* device_type,
                                         size_t* memory_mb,
                                         bool* has_gpu);

/**
 * 注册模型
 * 
 * @param adapter 适配器句柄
 * @param model_name 模型名称
 * @param model_size_mb 模型大小（MB）
 * @param required_memory_gb 所需内存（GB）
 * @return 成功返回LINGZHU_OK，失败返回错误码
 */
LingzhuError lingzhu_edge_register_model(LingzhuEdgeAdapter* adapter,
                                          const char* model_name,
                                          float model_size_mb,
                                          float required_memory_gb);

/**
 * 自适应推理
 * 
 * @param adapter 适配器句柄
 * @param model_name 模型名称
 * @param input_json 输入数据（JSON字符串）
 * @param output_json 输出数据（JSON字符串，调用者负责释放）（输出）
 * @return 成功返回LINGZHU_OK，失败返回错误码
 */
LingzhuError lingzhu_edge_adapt_inference(LingzhuEdgeAdapter* adapter,
                                            const char* model_name,
                                            const char* input_json,
                                            char** output_json);

// ==================== 三进制逻辑 ====================

/**
 * Trit逻辑运算：最小值
 * 
 * @param a Trit a
 * @param b Trit b
 * @return min(a, b)
 */
LingzhuTrit lingzhu_ternary_min(LingzhuTrit a, LingzhuTrit b);

/**
 * Trit逻辑运算：最大值
 * 
 * @param a Trit a
 * @param b Trit b
 * @return max(a, b)
 */
LingzhuTrit lingzhu_ternary_max(LingzhuTrit a, LingzhuTrit b);

/**
 * Trit逻辑运算：中值
 * 
 * @param a Trit a
 * @param b Trit b
 * @return mid(a, b) = he
 */
LingzhuTrit lingzhu_ternary_mid(LingzhuTrit a, LingzhuTrit b);

/**
 * Trit移位运算
 * 
 * @param a Trit a
 * @param shift 移位量（-1, 0, +1）
 * @return shifted Trit
 */
LingzhuTrit lingzhu_ternary_shift(LingzhuTrit a, int shift);

// ==================== 卦象19683 ====================
#define LINGZHU_HEXAGRAM_LENGTH 9  // 9位三进制

typedef struct {
    LingzhuTrit trits[LINGZHU_HEXAGRAM_LENGTH];
} LingzhuHexagram19683;

/**
 * 初始化卦象（全为he）
 * 
 * @param hexagram 卦象指针
 */
void lingzhu_hexagram_init(LingzhuHexagram19683* hexagram);

/**
 * 随机生成卦象
 * 
 * @param hexagram 卦象指针
 */
void lingzhu_hexagram_randomize(LingzhuHexagram19683* hexagram);

/**
 * 从字符串加载卦象
 * 
 * @param hexagram 卦象指针
 * @param str 9字符字符串（如"-0+-0+-0+"）
 * @return 成功返回LINGZHU_OK，失败返回错误码
 */
LingzhuError lingzhu_hexagram_from_string(LingzhuHexagram19683* hexagram, 
                                           const char* str);

/**
 * 转换为字符串
 * 
 * @param hexagram 卦象指针
 * @param str 输出字符串（至少10字节）（输出）
 */
void lingzhu_hexagram_to_string(LingzhuHexagram19683* hexagram, char* str);

/**
 * 获取卦象的π坐标
 * 
 * @param hexagram 卦象指针
 * @return π坐标（double）
 */
double lingzhu_hexagram_pi_coordinate(LingzhuHexagram19683* hexagram);

/**
 * 获取卦象的e时间戳
 * 
 * @param hexagram 卦象指针
 * @return e时间戳（uint64_t）
 */
uint64_t lingzhu_hexagram_e_timestamp(LingzhuHexagram19683* hexagram);

// ==================== 版本和错误处理 ====================

/**
 * 获取SDK版本字符串
 * 
 * @return 版本字符串（如"V185.0"）
 */
const char* lingzhu_get_version();

/**
 * 获取错误描述
 * 
 * @param error 错误码
 * @return 错误描述字符串
 */
const char* lingzhu_get_error_string(LingzhuError error);

#ifdef __cplusplus
}
#endif

#endif // LINGZHU_SDK_H