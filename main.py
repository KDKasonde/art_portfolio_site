from website import create_website

website = create_website()

if __name__ == '__main__':
    website.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

