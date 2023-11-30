const appData = {
    sortCol: null,
    sortAsc: true,
    pageSize: 10,
    currPage: 1,
    reviews,
    sort(col) {
        if (this.sortCol === col) this.sortAsc = !this.sortAsc;
        this.sortCol = col;
        this.reviews.sort((a, b) => {
            if (a[this.sortCol] < b[this.sortCol]) return this.sortAsc ? 1 : -1;
            if (a[this.sortCol] > b[this.sortCol]) return this.sortAsc ? -1 : 1;
            return 0;
        });
    },
    get totalPages() {
        return Math.ceil(this.reviews.length / this.pageSize);
    },
    get isPreviousPage() {
        return this.currPage > 1;
    },
    get isNextPage() {
        return (this.currPage * this.pageSize) < this.reviews.length;
    },
    nextPage() {
        if (this.isNextPage) this.currPage++;
    },
    previousPage() {
        if (this.isPreviousPage) this.currPage--;
    },
    get start() {
        return (this.currPage - 1) * this.pageSize;
    },
    get end() {
        return this.currPage * this.pageSize;
    },
    get pagedReviews() {
        if (!this.reviews) return [];
        return this.reviews.slice(this.start, this.end);
    },
    get visiblePages() {
        let pages = [];
        let startPage, endPage;

        if (this.totalPages <= 5) {
            startPage = 1;
            endPage = this.totalPages;
        } else {
            if (this.currPage <= 3) {
                startPage = 1;
                endPage = 5;
            } else if (this.currPage + 2 >= this.totalPages) {
                startPage = this.totalPages - 4;
                endPage = this.totalPages;
            } else {
                startPage = this.currPage - 2;
                endPage = this.currPage + 2;
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            pages.push(i);
        }

        if (endPage < this.totalPages - 2) {
            pages.push('...');
            pages.push(this.totalPages - 1);
            pages.push(this.totalPages);
        } else if (endPage < this.totalPages) {
            pages.push(this.totalPages);
        }

        return pages;
    },
    goToPage(page) {
        if (page !== '...') {
            this.currPage = page;
        }
    }
}
