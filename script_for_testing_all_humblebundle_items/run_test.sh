export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."
echo 'This test will determine how amazon books scraper library works for all current humblebundle books!'
echo 'Now it will download info about books from humblebundle website'
python fetch_humblebundle_info.py
echo 'Now fetching amazon info for books begins'
python get_amazon_info_for_books.py