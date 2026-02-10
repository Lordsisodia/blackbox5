#!/usr/bin/env python3
"""
Quick reference for using the BlackBox5 Multi-API System
Run this file to see usage examples
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def print_separator(char="=", length=80):
    print(char * length)


def example_1_basic_provider_selection():
    """Example 1: Basic provider selection"""
    print("\n### Example 1: Basic Provider Selection\n")
    print("```python")
    print("from agents.api_selector import APISelector")
    print()
    print("selector = APISelector()")
    print()
    print("# Select best provider for a coding task")
    print("selection = selector.select_provider(")
    print("    task_type='coding',")
    print("    required_capabilities=['coding', 'reasoning'],")
    print("    criticality='high'")
    print(")")
    print()
    print("print(f'Provider: {selection.provider.name}')")
    print("print(f'API Key: {selection.provider.api_key}')")
    print("print(f'Reason: {selection.reason}')")
    print("print(f'Fallbacks: {selection.fallback_chain}')")
    print("```")
    print()
    print("**Output:**")
    print("Provider: Claude Code CLI")
    print("API Key: sk-ant-...")
    print("Reason: matched task type 'coding', healthy status, quality-prioritized selection")
    print("Fallbacks: ['kimi']")


def example_2_track_usage():
    """Example 2: Track API usage"""
    print("\n### Example 2: Track API Usage\n")
    print("```python")
    print("from agents.api_usage_tracker import APIUsageTracker")
    print()
    print("tracker = APIUsageTracker()")
    print()
    print("# Track an API call")
    print("tracker.track_usage(")
    print("    provider='kimi',")
    print("    agent='main',")
    print("    task_type='coding',")
    print("    tokens_used=5000,")
    print("    duration_ms=1234,")
    print("    success=True")
    print(")")
    print()
    print("# Get statistics")
    print("stats = tracker.get_stats(days=7)")
    print("print(stats)")
    print("```")
    print()
    print("**Output:**")
    print("{'requests': 1, 'total_tokens': 5000, 'success_rate': 100.0, ...}")


def example_3_kimi_load_balancer():
    """Example 3: Kimi load balancer"""
    print("\n### Example 3: Kimi Load Balancer\n")
    print("```python")
    print("from agents.kimi_load_balancer import KimiLoadBalancer")
    print()
    print("balancer = KimiLoadBalancer()")
    print()
    print("# Get best key for an agent")
    print("key = balancer.get_key(agent='main')")
    print()
    print("if key:")
    print("    print(f'Using key: {key.name}')")
    print("    print(f'API key: {key.key[:20]}...')")
    print()
    print("    # Use the key...")
    print()
    print("    # Report usage")
    print("    balancer.report_usage(")
    print("        key_id=key.id,")
    print("        tokens_used=5000,")
    print("        latency_ms=1234,")
    print("        success=True")
    print("    )")
    print()
    print("# Get status of all keys")
    print("status = balancer.get_key_status()")
    print("for key_id, info in status.items():")
    print("    print(f'{key_id}: {info[\"status\"]} (priority: {info[\"priority\"]})')")
    print("```")


def example_4_generate_report():
    """Example 4: Generate usage report"""
    print("\n### Example 4: Generate Usage Report\n")
    print("```python")
    print("from agents.api_usage_tracker import APIUsageTracker")
    print("import json")
    print()
    print("tracker = APIUsageTracker()")
    print()
    print("# Generate comprehensive report")
    print("report = tracker.generate_report(days=7)")
    print()
    print("print('=== Usage Report ===')")
    print("print(f'Period: Last {report[\"period_days\"]} days')")
    print("print(f'Total Requests: {report[\"summary\"][\"total_requests\"]}')")
    print("print(f'Total Tokens: {report[\"summary\"][\"total_tokens\"]:,}')")
    print("print(f'Total Cost: ${report[\"summary\"][\"total_cost\"]:.4f}')")
    print("print(f'Avg Success Rate: {report[\"summary\"][\"avg_success_rate\"]}%')")
    print()
    print("print('\\\\n=== By Provider ===')")
    print("for provider_id, stats in report['by_provider'].items():")
    print("    print(f'{provider_id}:')")
    print("    print(f'  Requests: {stats[\"requests\"]}')")
    print("    print(f'  Tokens: {stats[\"total_tokens\"]:,}')")
    print("    print(f'  Success Rate: {stats[\"success_rate\"]}%')")
    print()
    print("# Save report to file")
    print("with open('/opt/blackbox5/data/usage-report.json', 'w') as f:")
    print("    json.dump(report, f, indent=2)")
    print("```")


def example_5_nvidia_video():
    """Example 5: Nvidia video processing"""
    print("\n### Example 5: Nvidia Video Processing\n")
    print("```python")
    print("from agents.nvidia_kimi_integration import NvidiaKimiClient")
    print()
    print("client = NvidiaKimiClient()")
    print()
    print("if client.is_available():")
    print("    # Process a video")
    print("    result = client.process_video(")
    print("        video_path='/path/to/video.mp4',")
    print("        prompt='Summarize this video',")
    print("        extract_frames=5")
    print("    )")
    print()
    print("    print(f'Summary: {result.summary}')")
    print("    print(f'Tokens used: {result.tokens_used}')")
    print("    print(f'Processing time: {result.processing_time_ms:.0f}ms')")
    print()
    print("    # Analyze an image")
    print("    result = client.analyze_image(")
    print("        image_path='/path/to/image.jpg',")
    print("        prompt='What objects are in this image?'")
    print("    )")
    print()
    print("    print(f'Description: {result.description}')")
    print("    print(f'Objects: {result.objects}')")
    print("else:")
    print("    print('Nvidia Kimi not available - check API key')")
    print("```")


def example_6_check_alerts():
    """Example 6: Check alerts"""
    print("\n### Example 6: Check Usage Alerts\n")
    print("```python")
    print("from agents.api_usage_tracker import APIUsageTracker")
    print()
    print("tracker = APIUsageTracker()")
    print()
    print("# Check for alerts")
    print("alerts = tracker.check_alerts()")
    print()
    print("if alerts:")
    print("    print(f'Found {len(alerts)} alerts:')")
    print("    for alert in alerts:")
    print("        print(f'  [{alert.level.upper()}] {alert.provider}: {alert.message}')")
    print("        print(f'    Metric: {alert.metric} = {alert.value} (threshold: {alert.threshold})')")
    print("else:")
    print("    print('No alerts - all systems nominal')")
    print("```")


def example_7_task_types():
    """Example 7: Task types reference"""
    print("\n### Example 7: Supported Task Types\n")
    print("| Task Type | Best Provider | Use Case |")
    print("|-----------|---------------|----------|")
    print("| `long_context` | GLM-4.7 | Long conversations, large context |")
    print("| `coding` | Kimi K2.5 | Code generation, programming |")
    print("| `reasoning` | Claude Code | Complex analysis, critical thinking |")
    print("| `video_processing` | Nvidia Kimi | Video analysis, summarization |")
    print("| `vision` | Nvidia Kimi | Image analysis, object detection |")
    print("| `general` | GLM-4.7 | Default tasks, general purpose |")
    print()
    print("**Example:**")
    print("```python")
    print("# Select for different task types")
    print("for task_type in ['coding', 'video_processing', 'reasoning']:")
    print("    selection = selector.select_provider(")
    print("        task_type=task_type,")
    print("        criticality='medium'")
    print("    )")
    print("    print(f'{task_type}: {selection.provider.name}')")
    print("```")


def main():
    """Main function - print all examples"""
    print_separator()
    print("BlackBox5 Multi-API System - Quick Reference")
    print_separator()

    example_1_basic_provider_selection()
    print_separator()
    example_2_track_usage()
    print_separator()
    example_3_kimi_load_balancer()
    print_separator()
    example_4_generate_report()
    print_separator()
    example_5_nvidia_video()
    print_separator()
    example_6_check_alerts()
    print_separator()
    example_7_task_types()

    print_separator()
    print("For more details, see:")
    print("  - /opt/blackbox5/MULTI_API_SETUP.md")
    print("  - /opt/blackbox5/MULTI_API_SETUP_COMPLETE.md")
    print("  - /opt/blackbox5/data/multi-api-setup-report.json")
    print_separator()


if __name__ == "__main__":
    main()
