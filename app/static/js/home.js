const appData = {
    productUrl: '',
    loading: false,
    error: '',
    errorToMessage(error) {
        return {
            'productUrl.empty': 'Please enter a product URL.',
        }[error] || 'Something went wrong. Please try again later.'
    },
    get isLoading() {
        return this.loading;
    },
    async startScraping() {
        this.loading = true;
        this.error = '';
        try {
            await axios.post('/api/products', {
                productUrl: this.productUrl,
            });
        } catch (e) {
            this.error = this.errorToMessage(e.response.data.message)
        } finally {
            this.loading = false;
        }
    }
}
