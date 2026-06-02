const Fuse = require('fuse.js');
const fs = require('fs');

const data = JSON.parse(fs.readFileSync('web/search_index.json', 'utf8'));
const fuse = new Fuse(data, {
    keys: ['title', 'content'],
    includeMatches: true,
    threshold: 0.3,
    ignoreLocation: true
});

console.log("Search for '결제':");
console.log(fuse.search('결제').length + ' results');

console.log("Search for '플렉스지':");
console.log(fuse.search('플렉스지').length + ' results');
