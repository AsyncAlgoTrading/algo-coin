module.exports = {
  verbose: true,
  transform: {
    "^.+\\.(ts|tsx)$": "ts-jest",
    ".+\\.(css|styl|less|sass|scss)$": "jest-transform-css"
  },
  cache: false,
  testPathIgnorePatterns: [
    "__tests__/js"
  ],
  transformIgnorePatterns: [
    "node_modules"
  ],
  moduleNameMapper:{
      "\\.(css|less)$": "<rootDir>/__tests__/js/styleMock.js",
      "\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$": "<rootDir>/__tests__/js/fileMock.js"
  },
  preset: 'ts-jest'
};
