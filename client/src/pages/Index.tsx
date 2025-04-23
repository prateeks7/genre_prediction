
import React, { useState } from "react";
import SongRecommendationCard from "../components/SongRecommendationCard";
import { Search, ListMusic } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type Song = {
  title: string;
  artist: string;
  genre: string;
};

// const mockSongs: Song[] = [
//   { title: "Purple Skies", artist: "DJ Lavender", genre: "Pop" },
//   { title: "Neon Nights", artist: "The Electrics", genre: "Synthwave" },
//   { title: "Smooth Waves", artist: "Mellow Beats", genre: "Chill" },
//   { title: "Sunset Groove", artist: "Funky Trails", genre: "Funk" },
//   { title: "Stellar Dreams", artist: "Lunar Harmony", genre: "Indie" },
//   { title: "Midnight Melody", artist: "Soul Surfers", genre: "Soul" },
//   { title: "Echoes", artist: "Reverb Nation", genre: "Rock" },
//   { title: "Moonlit Walk", artist: "Night Sky", genre: "R&B" },
//   { title: "Breeze", artist: "The Daydreamers", genre: "Pop" },
//   { title: "Golden Touch", artist: "Shimmering Sound", genre: "Electronic" },
// ];

const Index = () => {
  const [mockSongs, setSongs] = useState([]);
  const [url, setUrl] = useState("");
  const [showRecommendations, setShowRecommendations] = useState(false);

  const handleRecommend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim() === "") return;
    try {
      const response = await fetch("http://localhost:5050/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({url:url})
      });

      const data = await response.json();

      console.log(data.result)
      setSongs(data.result);
      // console.log("Recommendation:", data.result);
    } catch (error) {
      console.error("Error:", error);
    }
    setShowRecommendations(true);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(e.target.value);
    if(showRecommendations) setShowRecommendations(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-purple-100 transition-colors">
      <div className="w-full max-w-xl">
        <div className="bg-white/95 rounded-2xl shadow-lg p-8">
          <div className="flex items-center gap-2 mb-8">
            <ListMusic className="text-purple-500" size={32} />
            <h1 className="text-3xl sm:text-4xl font-extrabold text-purple-700 tracking-tight">
              FMA Recommendations Hub
            </h1>
          </div>

          {!showRecommendations ? (
            <form onSubmit={handleRecommend} className="flex flex-col gap-6">
              <label className="text-lg font-medium text-gray-700 text-left">
                Paste a youtube song URL
              </label>
              <div className="flex gap-2">
                <Input
                  type="url"
                  value={url}
                  onChange={handleInputChange}
                  placeholder="e.g. https://www.youtube.com/watch?..."
                  className="flex-1 border-purple-200 bg-purple-50 focus:ring-2 focus:ring-purple-500"
                  required
                />
                <Button
                  type="submit"
                  size="lg"
                  disabled={!url.trim()}
                  className="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-2 rounded-lg transition-colors shadow-sm flex items-center gap-2"
                >
                  <Search size={20} />
                  Recommend
                </Button>
              </div>
              <div className="text-sm text-gray-400 mt-2">
                We'll recommend you 10 songs you might love!
              </div>
            </form>
          ) : (
            <div className="fade-in">
              <div className="mb-6">
                <h2 className="text-xl font-bold text-gray-800 mb-1">
                  Top 10 Song Recommendations
                </h2>
                <div className="text-sm text-gray-500 mb-2 truncate">
                  for URL: <span className="font-mono">{url}</span>
                </div>
              </div>
              <div>
                {mockSongs.map((song, i) => (
                  <SongRecommendationCard key={i} song={song} index={i} />
                ))}
              </div>
              <Button
                variant="outline"
                className="mt-6"
                onClick={() => setShowRecommendations(false)}
              >
                Try another URL
              </Button>
            </div>
          )}
        </div>
        <div className="mt-8 text-center text-gray-400 text-xs">
          © {new Date().getFullYear()} FMA Recommendations Hub
        </div>
      </div>
      <style>
        {`
          .fade-in {
            animation: fadeIn 0.7s cubic-bezier(.39,.58,.57,1.25);
          }
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(12px);}
            to { opacity: 1; transform: translateY(0);}
          }
        `}
      </style>
    </div>
  );
};

export default Index;
