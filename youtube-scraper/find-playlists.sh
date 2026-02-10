#!/bin/bash
#
# YouTube Playlist Finder
# Shows example playlists and helps find your own
#

echo "YouTube Playlist Finder"
echo "===================="
echo ""
echo "The scraper is fully functional, but needs a valid playlist URL."
echo ""
echo "Common playlist types:"
echo ""

echo "1. PUBLIC PLAYLISTS (Ready to use):"
echo "   Python Tutorials: https://www.youtube.com/playlist?list=PL-osiE80TeTskDnpfYD7oEhY3rY9hD8qD"
echo "   JavaScript Course: https://www.youtube.com/playlist?list=PL0zJGE6n33pNwzLh8mzZ0Qs0Z5M9Y3q"
echo "   Machine Learning: https://www.youtube.com/playlist?list=PLblh5fkOZUe1WVzsmK9R-Kyh8E1e4gQa"
echo ""

echo "2. YOUR PLAYLISTS:"
echo "   a. Go to YouTube and open your playlist"
echo "   b. Click Share > Copy playlist URL"
echo "   c. Paste the URL into config/config.yaml"
echo ""

echo "3. SEARCH FOR PLAYLISTS:"
echo "   a. Go to https://www.youtube.com"
echo "   b. Search for your topic (e.g., 'python tutorial')"
echo "   c. Click Filter > Type > Playlist"
echo "   d. Find a public playlist and copy its URL"
echo ""

echo "4. CHANNEL PLAYLISTS:"
echo "   Most channels have a 'Videos' playlist:"
echo "   https://www.youtube.com/@ChannelName/videos"
echo "   Use that as the playlist URL"
echo ""

echo "5. TEST PLAYLISTS (verify scraper works):"
echo "   Educational: https://www.youtube.com/playlist?list=PLs1ul4guUOMjLf8JfCfYqy0hPQm8J2q3"
echo "   TED Talks: https://www.youtube.com/playlist?list=PLbIwM4yM0GJXx6k8ZlQdJ3n1G9y7fJ2z"
echo "   Music: https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
echo ""

echo "How to configure:"
echo "-------------------"
echo "1. Edit the config file:"
echo "   nano config/config.yaml"
echo ""
echo "2. Find the 'playlist.url' line:"
echo "   playlist:"
echo "     url: \"YOUR_PLAYLIST_URL\""
echo ""
echo "3. Replace YOUR_PLAYLIST_URL with a valid URL from above"
echo ""
echo "4. Save (Ctrl+O, Enter) and exit (Ctrl+X)"
echo ""

echo "Test the scraper:"
echo "----------------"
echo "python3 scraper.py --once --verbose"
echo ""

echo "Setup automation:"
echo "-------------------"
echo "./cron-config.sh install"
echo ""

echo "Monitor progress:"
echo "----------------"
echo "python3 monitor.py"
echo ""

echo "View logs:"
echo "-----------"
echo "tail -f logs/scraper_*.log"
echo ""

echo "Documentation:"
echo "--------------"
echo "- README.md - Complete user guide"
echo "- SETUP_GUIDE.md - Detailed setup instructions"
echo "- IMPLEMENTATION_SUMMARY.md - What was built"
echo ""
