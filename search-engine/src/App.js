import "./App.css";
import React, { useState } from "react";
import axios from "axios";

function App() {
  // State variables
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [resultCount, setResultCount] = useState(0);

  // Function to perform search request
  const searchResult = async (query) => {
    try {
      // Send GET request to the search API endpoint
      const response = await axios.get(`http://127.0.0.1:8000/search/${query}`);
      const results = response.data.query;
      setSearchResults(results);
    } catch (error) {
      console.error("Error occurred while searching:", error);
      // Handle the error
    }
  };

  // Function to capitalize the first letter of a string
  function capitalizeFirstLetter(string) {
    if (!string) {
      return string;
    }
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  // Function to convert a sentence to title case
  function convertToTitleCase(sentence) {
    if (!sentence) {
      return sentence;
    }

    const words = sentence.split(" ");
    const capitalizedWords = words.map((word) => {
      return word.charAt(0).toUpperCase() + word.slice(1);
    });

    return capitalizedWords.join(" ");
  }

  return (
    <div className="">
      <div className="p-10 w-full justify-center items-center flex flex-col">
        <img src="/logo.png" alt="Logo" />
        {/* Search input */}
        <div className="mt-3 overflow-hidden rounded-lg flex md:w-1/2 w-full ">
          <input
            type="search"
            name="search"
            placeholder="Search..."
            className="border-2 w-full px-4 py-2 rounded-l-lg focus:outline-none"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            className="p-2 w-1/6 bg-blue-900 text-white border border-blue-900 text-lg rounded-r-lg"
            onClick={() => {
              searchResult(query);
            }}
          >
            Search
          </button>
        </div>
      </div>
      <div className="p-10">
        {/* Display result count if available */}
        {resultCount && resultCount > 0 ? (
          <p className="text-base text-gray-400">
            Search results: {resultCount} results found
          </p>
        ) : (
          <p className="text-base text-gray-400">Search results</p>
        )}

        {/* Display search results */}
        {searchResults?.length > 0 ? (
          <ul>
            {searchResults?.map((value, index) => (
              <li key={index} className="border rounded-md p-3 my-3">
                {/* Title */}
                <h1 className="text-black-700 font-bold hover:underline w-fit">
                  {convertToTitleCase(value?.title)}
                </h1>

                {/* Author */}
                <h1 className="text-green-800 text-sm">
                  Author: {capitalizeFirstLetter(value?.Cov_Uni_Author)}
                </h1>

                {/* URL */}
                <p className="text-blue-700">
                  <a
                    href={value?.URL}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {value?.URL}
                  </a>
                </p>

                {/* Date */}
                <h1 className="text-sm">{value?.Date}</h1>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-3 text-lg">No Results found</p>
        )}
      </div>
    </div>
  );
}

export default App;
