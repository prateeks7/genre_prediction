
import { Music } from "lucide-react";

type Song = {
  title: string;
  artist: string;
  genre: string;
};

const SongRecommendationCard = ({ song, index }: { song: Song; index: number }) => (
  <div className="flex items-center bg-white rounded-lg shadow p-4 mb-4 transition-transform hover:scale-[1.017] border border-gray-100">
    <div className="flex-shrink-0 mr-4 rounded-full bg-purple-100 p-2">
      <Music className="text-purple-500" size={32} />
    </div>
    <div>
      <div className="font-semibold text-lg text-gray-800">{index + 1}. {song.title}</div>
      <div className="text-sm text-gray-500">{song.artist}</div>
      <div className="text-xs mt-1 px-2 py-0.5 bg-purple-50 text-purple-700 rounded inline-block">{song.genre}</div>
    </div>
  </div>
);

export default SongRecommendationCard;
