#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Pipeline 运行脚本
快速启动和运行 Pipeline 的示例
'''

from xparse_pipeline import create_pipeline_from_config, S3Source, LocalSource, MilvusDestination, LocalDestination, Pipeline


# ============================================================================
# 方式 1: 使用配置字典
# ============================================================================

def run_with_config():
    """使用配置字典运行 pipeline"""
    
    config = {
        'source': {
            'type': 's3',
            'endpoint': 'https://textin-minio-api.ai.intsig.net',
            'access_key': 'IEQspf8C7fVcgmp3AZWl',
            'secret_key': 'kLj96I8FGbIrPFW08meXivCy4AVdzBijOJWKWOt1',
            'bucket': 'textin-test',
            'prefix': '',  # 留空处理所有文件，或指定如 'milvus/'
            'region': 'us-east-1'
        },
        'destination': {
            'type': 'milvus',
            'db_path': './milvus_pipeline.db',
            'collection_name': 'pipeline_collection',
            'dimension': 1024
        },
        'api_base_url': 'https://api.textin.com/api/xparse',
        'api_headers': {
            'x-ti-app-id': '',
            'x-ti-secret-code': ''
        },
        # Parse 配置（可选）
        'parse_config': {},
        # Chunk 配置（可选）
        'chunk_config': {
            'strategy': 'basic',              # 分块策略: 'basic' | 'by_title' | 'by_page'
            'include_orig_elements': False,   # 是否包含原始元素
            'new_after_n_chars': 512,         # 多少字符后创建新块
            'max_characters': 1024,           # 最大字符数
            'overlap': 0                      # 重叠字符数
        },
        # Embed 配置（可选）
        'embed_config': {
            'provider': 'qwen',                    # 向量化供应商: 'qwen'
            'model_name': 'text-embedding-v3'      # 模型名称: 'text-embedding-v3' | 'text-embedding-v4'
        }
    }
    
    pipeline = create_pipeline_from_config(config)
    pipeline.run()


# ============================================================================
# 方式 2: 手动创建组件
# ============================================================================

def run_with_manual_setup():
    """手动创建 Source、Destination 和 Pipeline"""
    from xparse_pipeline import ChunkConfig, EmbedConfig, ParseConfig
    
    # 创建 S3 数据源
    source = S3Source(
        endpoint='https://textin-minio-api.ai.intsig.net',
        access_key='IEQspf8C7fVcgmp3AZWl',
        secret_key='kLj96I8FGbIrPFW08meXivCy4AVdzBijOJWKWOt1',
        bucket='textin-test',
        prefix='',
        region='us-east-1'
    )
    
    # 创建 Milvus 目的地
    destination = MilvusDestination(
        db_path='./milvus_pipeline.db',
        collection_name='pipeline_collection',
        dimension=1024
    )
    
    # 创建配置对象
    parse_config = ParseConfig()
    
    chunk_config = ChunkConfig(
        strategy='by_title',           # 按标题分块
        include_orig_elements=False,
        new_after_n_chars=512,
        max_characters=1024,
        overlap=50                     # 块之间重叠 50 字符
    )
    
    embed_config = EmbedConfig(
        provider='qwen',
        model_name='text-embedding-v3'
    )
    
    # 创建 Pipeline
    pipeline = Pipeline(
        source=source,
        destination=destination,
        api_base_url='https://api.textin.com/api/xparse',
        api_headers={
            'x-ti-app-id': '',
            'x-ti-secret-code': ''
        },
        parse_config=parse_config,
        chunk_config=chunk_config,
        embed_config=embed_config
    )
    
    # 运行
    pipeline.run()


# ============================================================================
# 方式 3: 本地测试（本地文件 -> 本地输出）
# ============================================================================

def run_local_test():
    """使用本地文件进行测试"""
    
    config = {
        'source': {
            'type': 'local',
            'directory': '/Users/ke_wang/Documents/doc',
            'pattern': '*.pdf'
        },
        'destination': {
            'type': 'local',
            'output_dir': './test_output'
        },
        'api_base_url': 'https://api.textin.com/api/xparse',
        'api_headers': {
            'x-ti-app-id': '',
            'x-ti-secret-code': ''
        },
        # Parse 配置（可选）
        'parse_config': {},
        # Chunk 配置（可选）
        'chunk_config': {
            'strategy': 'basic',
            'include_orig_elements': False,
            'new_after_n_chars': 512,
            'max_characters': 1024,
            'overlap': 0
        },
        # Embed 配置（可选）
        'embed_config': {
            'provider': 'qwen',
            'model_name': 'text-embedding-v3'
        }
    }
    
    pipeline = create_pipeline_from_config(config)
    pipeline.run()


# ============================================================================
# 方式 4: 处理单个文件
# ============================================================================

def run_single_file():
    """只处理单个文件"""
    from xparse_pipeline import ChunkConfig, EmbedConfig, ParseConfig
    
    # 创建 pipeline
    source = LocalSource(directory='/Users/ke_wang/Documents/doc', pattern='*.pdf')
    destination = LocalDestination(output_dir='./output')
    
    # 创建配置
    chunk_config = ChunkConfig(
        strategy='by_page',            # 按页面分块
        max_characters=2048,           # 增大块大小
        overlap=100
    )
    
    embed_config = EmbedConfig(
        provider='qwen',
        model_name='text-embedding-v4'  # 使用更高精度的模型
    )
    
    pipeline = Pipeline(
        source=source,
        destination=destination,
        api_base_url='https://api.textin.com/api/xparse',
        api_headers={
            'x-ti-app-id': '',
            'x-ti-secret-code': ''
        },
        chunk_config=chunk_config,
        embed_config=embed_config
    )
    
    # 只处理指定文件
    file_path = '4e3250f00210431fb29ca0c808.pdf'  # 相对于 source directory 的路径
    success = pipeline.process_file(file_path)
    
    if success:
        print(f"\n✅ 文件 {file_path} 处理成功！")
    else:
        print(f"\n❌ 文件 {file_path} 处理失败！")


# ============================================================================
# 方式 5: 自定义处理流程
# ============================================================================

def run_custom_flow():
    """自定义处理流程，手动控制文件处理"""
    from xparse_pipeline import ChunkConfig, EmbedConfig
    
    # 创建组件
    source = S3Source(
        endpoint='https://textin-minio-api.ai.intsig.net',
        access_key='IEQspf8C7fVcgmp3AZWl',
        secret_key='kLj96I8FGbIrPFW08meXivCy4AVdzBijOJWKWOt1',
        bucket='textin-test',
        prefix='',
        region='us-east-1'
    )
    
    destination = MilvusDestination(
        db_path='./milvus_custom.db',
        collection_name='custom_collection',
        dimension=1024
    )
    
    # 自定义配置
    chunk_config = ChunkConfig(
        strategy='by_title',
        include_orig_elements=True,
        max_characters=1536,
        overlap=80
    )
    
    embed_config = EmbedConfig(
        provider='qwen',
        model_name='text-embedding-v4'
    )
    
    pipeline = Pipeline(
        source=source,
        destination=destination,
        api_base_url='https://api.textin.com/api/xparse',
        api_headers={
            'x-ti-app-id': '',
            'x-ti-secret-code': ''
        },
        chunk_config=chunk_config,
        embed_config=embed_config
    )
    
    # 手动控制文件处理
    files = source.list_files()
    
    for file_path in files[:2]:  # 只处理前2个文件
        print(f"\n处理: {file_path}")
        file_bytes = source.read_file(file_path)

        # 使用 pipeline 接口处理
        result = pipeline.process_with_pipeline(file_bytes, file_path)
        
        if result:
            embedded, stats = result
            print(f"  - 原始元素: {stats.original_elements}")
            print(f"  - 分块后: {stats.chunked_elements}")
            print(f"  - 向量化: {stats.embedded_elements}")
            
            # 写入
            metadata = {
                'file_name': file_path,
                'stats': {
                    'original_elements': stats.original_elements,
                    'chunked_elements': stats.chunked_elements,
                    'embedded_elements': stats.embedded_elements
                }
            }
            destination.write(embedded, metadata)
            print(f"✓ 完成: {file_path}")
        else:
            print(f"✗ 失败: {file_path}")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数 - 选择运行方式"""
    
    print("=" * 60)
    print("Pipeline 运行脚本")
    print("=" * 60)
    print("\n请选择运行方式：")
    print("1. 使用配置字典 (S3 -> Milvus) [基础配置]")
    print("2. 手动创建组件 (S3 -> Milvus) [按标题分块 + 自定义配置]")
    print("3. 本地测试 (本地文件 -> 本地输出) [基础配置]")
    print("4. 处理单个文件 [按页面分块 + V4模型]")
    print("5. 自定义处理流程 [手动控制 + 统计信息]")
    print()
    
    try:
        choice = input("请输入选项 (1-5) [默认: 1]: ").strip() or '1'
        
        if choice == '1':
            print("\n使用配置字典运行...")
            run_with_config()
        elif choice == '2':
            print("\n手动创建组件运行...")
            run_with_manual_setup()
        elif choice == '3':
            print("\n本地测试模式...")
            run_local_test()
        elif choice == '4':
            print("\n处理单个文件...")
            run_single_file()
        elif choice == '5':
            print("\n自定义处理流程...")
            run_custom_flow()
        else:
            print("无效的选项，使用默认方式运行...")
            run_with_config()
    
    except KeyboardInterrupt:
        print("\n\n用户中断执行")
    except Exception as e:
        print(f"\n程序异常: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

