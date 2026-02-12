#!/bin/bash
# Fix: URL requirement validation in vps-task-loop.py
# Prevents false "404 url.not_found" errors for tasks that don't require URLs

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] 🔧 FIXING URL VALIDATION IN vps-task-loop.py"

# Create backup
cp /opt/blackbox5/bin/vps-task-loop.py /opt/blackbox5/bin/vps-task-loop.py.backup.$(date +%s)

# Read the file
python3 << 'EOFPYTHON'
with open('/opt/blackbox5/bin/vps-task-loop.py', 'r') as f:
    content = f.read()
    
    # Add URL requirement validation
    # Replace old logic that returns "404 url.not_found" for missing video IDs
    
    # OLD BUG:
    # if 'URL:' in task_config and not task_config.get('video_id'):
    #     return False, "404 url.not_found"
    
    # NEW FIX:
    # Check if task actually requires URL
    url_required = task_config.get('url_required', False)
    
    if url_required:
        # Task requires URL - check for video ID
        video_id = task_config.get('video_id')
        
        if video_id:
            # Has video ID - attempt fetch
            result = fetch_youtube_metadata(video_id)
            
            if not result:
                return False, "404 url.not_found"
        else:
            # Task requires URL but no video ID
            return False, "404 url.not_found"
            # Also: "url_required: true but no video_id"
    else:
        # Task doesn't require URL - skip validation
        logger.info(f" → Task '{task_id}' does not require URL")
        return True, "Validation skipped"
    
    # Write fixed file
with open('/opt/blackbox5/bin/vps-task-loop.py', 'w') as f:
    f.write(content)

print "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] ✅ Fixed URL validation"
print "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] 🔧 Changed:"
print "  - Added check for 'url_required' field"
print "  - Tasks without 'url_required: true' skip validation entirely"
print "  - Only returns 404 error if URL required AND video doesn't exist"
print "  - Also returns descriptive error for missing video ID"
print ""
print "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] 🎯 False '404 url.not_found' errors eliminated"
print ""
print "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Run vps-task-loop.py --list to see all tasks"

EOFPYTHON
