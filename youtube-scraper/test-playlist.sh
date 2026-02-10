#!/bin/bash
#
# YouTube Playlist Tester
# Tests if a playlist is accessible and how many videos it contains
#
# Usage: ./test-playlist.sh [PLAYLIST_URL]
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to print colored output
print_header() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "$1"
}

# Check if URL provided
if [ -z "$1" ]; then
    print_header "YouTube Playlist Tester"
    echo ""
    echo "Usage: $0 [PLAYLIST_URL]"
    echo ""
    echo "Examples:"
    echo "  $0 'https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf'"
    echo "  $0 'https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID'"
    echo ""
    exit 1
fi

PLAYLIST_URL="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_header "Testing Playlist: $PLAYLIST_URL"
echo ""

# Extract playlist ID
if [[ $PLAYLIST_URL == *"list="* ]]; then
    PLAYLIST_ID=$(echo "$PLAYLIST_URL" | grep -oP 'list=\K[^&]+')
    print_info "Playlist ID: $PLAYLIST_ID"
    echo ""
else
    print_error "No playlist ID found in URL"
    exit 1
fi

# Test with cookies.txt if exists
COOKIE_OPTS=""
if [ -f "$SCRIPT_DIR/config/cookies.txt" ]; then
    COOKIE_OPTS="--cookies $SCRIPT_DIR/config/cookies.txt"
    print_info "Using cookies.txt for authentication"
    echo ""
fi

# Test 1: Try yt-dlp with flat extraction (fastest)
print_header "Test 1: Quick scan (flat extraction)"
echo ""

if yt-dlp $COOKIE_OPTS --flat-playlist --dump-single-json "$PLAYLIST_URL" 2>&1 | grep -q '"_type": "playlist"'; then
    VIDEO_COUNT=$(yt-dlp $COOKIE_OPTS --flat-playlist --dump-single-json "$PLAYLIST_URL" 2>&1 | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('entries', [])))" 2>/dev/null || echo "0")
    print_success "Playlist is accessible"
    print_info "Total videos: $VIDEO_COUNT"
    echo ""
else
    print_warning "Quick scan failed, trying detailed extraction..."
    echo ""
fi

# Test 2: Try full extraction
print_header "Test 2: Detailed extraction (slower, more info)"
echo ""

OUTPUT=$(yt-dlp $COOKIE_OPTS --dump-single-json --playlist-end 1 "$PLAYLIST_URL" 2>&1)

if echo "$OUTPUT" | grep -q '"_type": "playlist"'; then
    print_success "Playlist accessible via full extraction"

    # Extract info
    TITLE=$(echo "$OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('title', 'Unknown'))" 2>/dev/null || echo "Unknown")
    VIDEO_COUNT=$(echo "$OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('entries', [])))" 2>/dev/null || echo "0")

    print_info "Playlist title: $TITLE"
    print_info "Total videos: $VIDEO_COUNT"
    echo ""

    # Show first video
    FIRST_VIDEO=$(yt-dlp $COOKIE_OPTS --flat-playlist --dump-single-json "$PLAYLIST_URL" 2>&1 | python3 -c "import sys, json; data=json.load(sys.stdin); entries=data.get('entries', []); print(f\"{entries[0].get('title', 'N/A')} (ID: {entries[0].get('id', 'N/A')})\")" 2>/dev/null || echo "N/A")
    print_info "First video: $FIRST_VIDEO"
    echo ""

    print_success "✓ Playlist is ready to use!"
    echo ""
    print_info "Next steps:"
    echo "  1. Update config/config.yaml with this playlist URL"
    echo "  2. Run: python3 scraper.py --once"
    echo ""
    exit 0

elif echo "$OUTPUT" | grep -q "The playlist does not exist"; then
    print_error "Playlist does not exist"
    echo ""
    print_info "Possible causes:"
    echo "  - Playlist ID is incorrect"
    echo "  - Playlist is private or unlisted"
    echo "  - Playlist has been deleted"
    echo ""
    print_info "Solutions:"
    echo "  - Verify the playlist URL in your browser"
    echo "  - Check if the playlist is public"
    echo "  - Use cookies for authentication (see SETUP_GUIDE.md)"
    echo ""
    exit 1

elif echo "$OUTPUT" | grep -q "Sign in to confirm you're not a bot"; then
    print_error "YouTube bot protection detected"
    echo ""
    print_info "The playlist is accessible but requires authentication"
    echo ""
    print_info "Solution:"
    echo "  - Set up cookies.txt (see SETUP_GUIDE.md Option 2)"
    echo "  - Or use cookies_from_browser in config.yaml"
    echo ""
    exit 1

else
    print_error "Failed to access playlist"
    echo ""
    print_info "Error output:"
    echo "$OUTPUT" | head -10
    echo ""
    exit 1
fi
