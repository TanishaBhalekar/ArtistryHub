import React, { useState, useEffect } from "react";
// Graceful imports for Clerk auth & React Router if available in the host app
let ClerkAuth = {
  useUser: () => ({ isSignedIn: false, user: null }),
  SignedIn: ({ children }) => <>{children}</>,
  SignedOut: ({ children }) => <>{children}</>,
  SignInButton: ({ children }) => <button className="btn-auth">{children || "Sign In"}</button>,
  UserButton: () => <div className="w-9 h-9 rounded-full bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-xs font-bold">AH</div>
};

try {
  const clerk = require("@clerk/clerk-react");
  if (clerk) ClerkAuth = clerk;
} catch (e) {
  // Clerk fallback already configured
}

const { useUser, SignedIn, SignedOut, SignInButton, UserButton } = ClerkAuth;

// Curated Discovery Data Contracts strictly matching Stitch & DESIGN.md
const SPOTLIGHT_ARTWORK = {
  id: "spotlight-varanasi",
  title: "Varanasi: City of Sacred Light",
  artist: {
    name: "Vikram Adiga",
    title: "Master Concept Artist",
    avatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuAb28DVOfNfmlxxsjjobn9ORPMNv2KiNlQE_ND2GsFeV4zYd5sUpR07ZBaFgE1E_VKYRqIBaJW4hFkT-LpA8SMhB-M0sOHasVat7THjp-51DbyvBXumQtYEB4sU2LFKfpXQ_2IPwF2osBkZhsqqwXGcPGMm99Revc1Alnnd5RQReVb5oC1x04gm4NfmbIzPb0sceRK6Un_fPVPNFovEWOtCA2qtkrCC9E1RCVCbeftM5bhJVjICi7QeQI6JflcCU6THH2F8-siCs2O1"
  },
  medium: "Concept Art / Digital Matte",
  tags: ["#heritage", "#concept-art", "#digital-matte", "#atmospheric"],
  priceINR: 85000,
  formattedPrice: "₹ 85,000 INR",
  description: "A transcendent exploration of ancient architecture meeting ethereal luminescence. Vikram Adiga's masterful concept art captures the soul of the sacred river with unprecedented detail and atmospheric depth.",
  image: "https://lh3.googleusercontent.com/aida-public/AB6AXuAYCTNI-6h_vccteqzr4KAnCTtv9Xsk6Je6vhs10zr1OUxasDNJKodtVn9PQmbxApS0x2SkCRGqXKbr2Hl7vuOdis_zcvj94INOTZdMPw_8KXWvSWiFi01f1EpJzoMWGa5uB-otZhRcdjRkG1Oi-Ft8sfvjCsFj1ZJ48fb_oEjD6PLyo6kS03tbAHzc18Ga1tvP9_xTaHgOL24NU7yslWpfSLepCflWb1L00sefETYkZF4HA-i9-KaRZ_Io3k7KtNn5fDd9iGtxMurO"
};

const DISCOVERY_ARTWORKS = [
  {
    id: "art-1",
    title: "Cyberpunk District 9",
    category: "Digital 2D",
    medium: "Digital 2D",
    artist: "Sarah Jenkins",
    artistAvatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuCujWv0h6o-nUY1ogId9i4um9wkWAKAS5k7M9kFGgEABKgKeIEZZhOJCYWKcSBZZzZ9fmcton-P2cN9JOtGpedht9MTmF5K5ctM5g7UvTSckTjkMYj-ZeSRo62JSUYW9j-RiCoZsHkcJTwCdvZLXZ170hCj_MrBlb2lItng0ajMXdMKmgVDSJgQN65bcVDZUQHnfxGrE_rzOhwqUDjexT_7Cta0024nyLFLcIao6I6WKB_2Vsp9lVZLNq-BKaj83WuUzjRLuzywnATE",
    priceINR: 18500,
    tags: ["#neon", "#cyberpunk", "#scifi"],
    likes: 385,
    views: 1420,
    image: "https://lh3.googleusercontent.com/aida-public/AB6AXuAbpJg1FvdU16_7Ik-P4lUE86y3VL0qvk5uq2psBH1OXB2Zk8x-bo-SICsWkpZHDk9O25CoYv1wboYUGG6N9ltiljompwYDIwbVs8DnVKP5-u6PZEHOS2Ebhx76DHd5CHE4NWiFN0pxKzlJnqbefo2g95sNilRV7VeSRFjZw4ptkLrz8OxqpmxmuPASa6tRzEjgYAMhKsYNwUaQiD3gcDJVwzbmLcnEr0a-m-NGUSp1jOpk41i5oG57Mcmtgq-0gjkVcv4W3aSvzBa3"
  },
  {
    id: "art-2",
    title: "Celestial Sitarist",
    category: "3D Render",
    medium: "3D Render",
    artist: "Rohan Mehra",
    artistAvatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuDEzE2-tsDvfeWSsKef86d5yIxPjs6wJEhISbQkfIb0VTPc_yZdw-hyr4YuL8x95wi5Y7NvyXre2Zx7AboF3Wyk_8f68AP1FHxgwQSslXg8lo20TkTcyS9pqC_ghdmIeGYmCoVSVxm8VkJ8wH7jPiFKQhrqnMr_pJ0HDP-zr8B9tzXOQ6BvWwlBaSS856Qy1quuIz86C6qHA_IMTMCnbVUqrgwnnNiUVTIkpxNnAtJURlNAtvlEEI2zO3C-7O0jXEO7Bo_oM8jRWwqY",
    priceINR: 42000,
    tags: ["#surreal", "#3d", "#mythology"],
    likes: 512,
    views: 2100,
    image: "https://lh3.googleusercontent.com/aida-public/AB6AXuDi-GSoBckvIxFKiEVT1keyIUcAFlDMNtPl2Ui1NEc00Tnn_tIAqtFIusw3h2sGj_WRy3pdWfPHchXbSc3gqF1CtSZ_PicYk9M-7KcuTZR4nMLqzRZYaVgXmY7c6oE26Sv6ljdxmlLmTpFcQ7fpi3ZYg2FsTo8pTLvQKlKfrfBntncUTScK0QxiqkgJrMR1geuUdH3Jr_g8osOOLpzkDVkDi772o9_gzFQ9HUq6YfVD3ylJB9IYpXAi_oYUsEwd14I08508FzSsDu2D"
  },
  {
    id: "art-3",
    title: "Monsoon over Western Ghats",
    category: "Landscape",
    medium: "Digital Oil",
    artist: "Priya Nair",
    artistAvatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuCd_1JZoIn_u6-AXcPtgpN8aPmHjaVrZks9GvMfckKUx0ITgfKcSPV04RnTLn1hpKT76l-44S7PNZT6DGu2SC6Db2FlR5oN_M76GPRjQC7Zh81V_nZV8h9ip5nu3t8txPGTpGQxV_J2aBTl7cwfTGJ8CsT71ITjGyhhxkWW7c6qKMcD8pyN5fLjun_PrlRv0H9glOGpRv4C6p1rT8hXjWd0fYf7qvdy5NZZVHs-cVM1WFydOXSBDDzSX7-ceGNhZKtMhELm7kY6ok5O",
    priceINR: 12000,
    tags: ["#landscape", "#atmospheric", "#monsoon"],
    likes: 240,
    views: 980,
    image: "https://lh3.googleusercontent.com/aida-public/AB6AXuBr-AHkDWR_JQvwEyy0452iGoBpUmfJqaYOpSLjn84vz1-BVWXdn89NRY7BBNMVlPyZ_1VSjJFw1_gIL9JAalGOqae9Vb_MhcQLCfZnE5dueAgiAW2tag6sokEeJJUq_J3XIvfrvYyOZLhztyhMutcyfGY7UuJ0OWPu9wQwbZYm_dYLWZUfv5C18MBWJm14QHSrtdlmb61wZ-bU8eqrMrF5ffM-7yjGloY9rEeJ2Rrl1lj0FRYVG2N860fW2WCLCddkx270Me2U8iSf"
  },
  {
    id: "art-4",
    title: "Mecha Garuda Awakening",
    category: "Concept Art",
    medium: "Concept Art",
    artist: "K. Sengupta",
    artistAvatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuDECVtd60ODR00wYmXTRdAOYrVTr161e8R50ylPKoiW_xkvQCnXenC8OHhZagWyQUSXG1jvLLPmz9r_HnOiU2c5bHk9HuBs9xmVqbwd7vZ91mrI8T8SVWZ6nHMYulGT3K4AfXdZtosL-7TKqBEiwYclr0d3QjjSHFAjdmR5RIeNOFrb-tH6H0acfYZxllQTiqOzrj8cr1f8ck9fif0GGay7kgFIJa5QTkEHKJSUzy2VqqQWqZymFgn2IgsyBgWYCKCdewKW5RYVPDYA",
    priceINR: 65000,
    tags: ["#mythology", "#scifi", "#mecha"],
    likes: 890,
    views: 3400,
    image: "https://lh3.googleusercontent.com/aida-public/AB6AXuBPPx7WQerd66GpvJpbWFG7hG4mwpmoJhXsyyFXfV4R1nGprVfvDwzgHTOam6ItJI6REC76vuQvxIVnjuJuZZyzS-fwaL2GDAzojaCvhmK2nFsfnCYbeKuI1T9I3s9cuyCe8794DniXtpwgL_F0NWTiM5xR1boblsWG4bwPjQrBf9JR60-leT4LyA5ompAD5QcvmF5lwO2qKzGA53K5fk528_eytm0gTfMUpo_bBaHQSHbGF3P_aCq1JzVsr6vD8wLrSMOuphNkhTV4"
  },
  {
    id: "art-5",
    title: "Prism Fluid Dynamic",
    category: "3D Render",
    medium: "Generative 3D",
    artist: "Studio K",
    artistAvatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80",
    priceINR: 24000,
    tags: ["#abstract", "#geometry", "#ue5"],
    likes: 310,
    views: 1150,
    image: "https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?auto=format&fit=crop&w=800&q=80"
  },
  {
    id: "art-6",
    title: "The Weaver's Solitude",
    category: "Traditional Oil",
    medium: "Traditional Canvas",
    artist: "Ananya Das",
    artistAvatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=150&q=80",
    priceINR: 35000,
    tags: ["#portrait", "#realism", "#oil"],
    likes: 430,
    views: 1600,
    image: "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=800&q=80"
  }
];

const CATEGORIES = [
  "All Works",
  "Concept Art",
  "Digital 2D",
  "3D Render",
  "Traditional Oil",
  "Character Design",
  "Landscape",
  "Surrealism"
];

export default function Home() {
  const { isSignedIn, user } = useUser();
  const [theme, setTheme] = useState(() => localStorage.getItem("artistryhub-theme") || "dark");
  const [selectedCategory, setSelectedCategory] = useState("All Works");
  const [searchQuery, setSearchQuery] = useState("");
  const [viewMode, setViewMode] = useState("grid"); // 'grid' | 'list'
  const [likedArtworks, setLikedArtworks] = useState({});
  const [activeModalArtwork, setActiveModalArtwork] = useState(null);

  // Sync theme with DOM, localStorage, and html class
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("artistryhub-theme", theme);
  }, [theme]);

  // Keyboard shortcut ⌘K / Ctrl+K focus search
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        document.getElementById("discoverySearchInput")?.focus();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  const toggleLike = (artId, initialCount) => {
    setLikedArtworks((prev) => {
      const isLiked = prev[artId]?.liked;
      const count = prev[artId]?.count ?? initialCount;
      return {
        ...prev,
        [artId]: {
          liked: !isLiked,
          count: isLiked ? count - 1 : count + 1
        }
      };
    });
  };

  // Filter artworks by category & search query
  const filteredArtworks = DISCOVERY_ARTWORKS.filter((art) => {
    const matchesCategory =
      selectedCategory === "All Works" ||
      art.category.toLowerCase().includes(selectedCategory.toLowerCase()) ||
      art.medium.toLowerCase().includes(selectedCategory.toLowerCase()) ||
      art.tags.some((t) => t.toLowerCase().includes(selectedCategory.toLowerCase()));

    const matchesSearch =
      searchQuery.trim() === "" ||
      art.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      art.artist.toLowerCase().includes(searchQuery.toLowerCase()) ||
      art.tags.some((t) => t.toLowerCase().includes(searchQuery.toLowerCase()));

    return matchesCategory && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-[#0E0F12] text-[#F8FAFC] data-[theme=light]:bg-[#FAF9F6] data-[theme=light]:text-[#1A1A1E] transition-colors duration-300 font-sans antialiased selection:bg-amber-500/30 selection:text-amber-300">
      
      {/* =========================================================================
          1. TOP NAVIGATION (Sticky Glassmorphic Bar)
          ========================================================================= */}
      <header className="sticky top-0 z-50 w-full backdrop-blur-xl border-b transition-colors duration-300 bg-[#0E0F12]/85 border-white/10 data-[theme=light]:bg-[#FAF9F6]/90 data-[theme=light]:border-[#E6E3DD]">
        <div className="max-w-[1440px] mx-auto px-5 md:px-16 py-4 flex items-center justify-between gap-4">
          
          {/* Brand Logo */}
          <div className="flex items-center gap-3">
            <a href="/" className="font-serif text-2xl font-bold tracking-tight text-[#F8FAFC] data-[theme=light]:text-[#1A1A1E] flex items-center gap-1.5">
              Artistry<span className="text-[#E5A93C] data-[theme=light]:text-[#D96B43]">Hub</span>
            </a>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-7">
            <a href="/" className="font-semibold text-sm pb-1 border-b-2 text-[#E5A93C] border-[#E5A93C] data-[theme=light]:text-[#D96B43] data-[theme=light]:border-[#D96B43]">
              Explore
            </a>
            <a href="/dashboard" className="text-sm font-medium text-slate-400 hover:text-[#E5A93C] data-[theme=light]:text-stone-600 data-[theme=light]:hover:text-[#D96B43] transition-colors">
              Studio Dashboard
            </a>
            <a href="/commissions" className="text-sm font-medium text-slate-400 hover:text-[#E5A93C] data-[theme=light]:text-stone-600 data-[theme=light]:hover:text-[#D96B43] transition-colors">
              Commissions
            </a>
            <a href="/ai-studio" className="text-sm font-medium text-slate-400 hover:text-[#E5A93C] data-[theme=light]:text-stone-600 data-[theme=light]:hover:text-[#D96B43] transition-colors">
              AI Studio
            </a>
          </nav>

          {/* Centered Search Bar with ⌘K Badge */}
          <div className="hidden lg:flex items-center flex-1 max-w-md mx-6 relative">
            <svg className="w-4 h-4 absolute left-3.5 text-slate-400 data-[theme=light]:text-stone-500 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              id="discoverySearchInput"
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search artworks, artists, styles, or tags..."
              className="w-full bg-[#1A1D27]/70 data-[theme=light]:bg-[#FFFFFF] border border-white/10 data-[theme=light]:border-[#E6E3DD] rounded-full py-2 pl-10 pr-14 text-sm text-[#F8FAFC] data-[theme=light]:text-[#1A1A1E] focus:outline-none focus:ring-2 focus:ring-[#E5A93C] data-[theme=light]:focus:ring-[#D96B43] placeholder:text-slate-500 data-[theme=light]:placeholder:text-stone-400 transition-all shadow-sm"
            />
            <div className="absolute right-3.5 flex items-center justify-center bg-white/10 data-[theme=light]:bg-stone-200 border border-white/10 data-[theme=light]:border-stone-300 rounded px-1.5 py-0.5 pointer-events-none">
              <span className="text-[10px] font-bold text-slate-300 data-[theme=light]:text-stone-600">⌘K</span>
            </div>
          </div>

          {/* Right Trailing Controls: Theme Toggle & Clerk Auth */}
          <div className="flex items-center gap-3">
            {/* Theme Toggle Button */}
            <button
              onClick={toggleTheme}
              aria-label="Toggle Theme"
              className="p-2 rounded-full border border-white/10 data-[theme=light]:border-[#E6E3DD] bg-white/5 data-[theme=light]:bg-stone-100 hover:bg-white/10 data-[theme=light]:hover:bg-stone-200 transition-all text-[#E5A93C] data-[theme=light]:text-[#D96B43]"
            >
              {theme === "dark" ? (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                </svg>
              )}
            </button>

            {/* Clerk Authentication Integration */}
            <SignedIn>
              <div className="flex items-center gap-3">
                <a
                  href="/dashboard"
                  className="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-semibold border border-white/10 data-[theme=light]:border-[#E6E3DD] bg-white/5 data-[theme=light]:bg-stone-100 hover:bg-white/10 data-[theme=light]:hover:bg-stone-200 transition-colors"
                >
                  <svg className="w-3.5 h-3.5 text-[#E5A93C] data-[theme=light]:text-[#D96B43]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Upload Artwork
                </a>
                <UserButton afterSignOutUrl="/" />
              </div>
            </SignedIn>

            <SignedOut>
              <div className="flex items-center gap-2">
                <SignInButton mode="modal">
                  <button className="px-4 py-1.5 rounded-full text-xs font-semibold border border-white/15 data-[theme=light]:border-[#E6E3DD] bg-white/5 hover:bg-white/15 transition-colors">
                    Sign In
                  </button>
                </SignInButton>
                <a
                  href="/dashboard"
                  className="px-4 py-1.5 rounded-full text-xs font-semibold text-black bg-[#E5A93C] hover:bg-[#F59E0B] data-[theme=light]:text-white data-[theme=light]:bg-[#D96B43] data-[theme=light]:hover:bg-[#BD5630] transition-colors shadow-sm"
                >
                  Join Studio
                </a>
              </div>
            </SignedOut>
          </div>

        </div>
      </header>

      {/* =========================================================================
          2. HORIZONTAL CATEGORY FILTER PILL BAR
          ========================================================================= */}
      <div className="sticky top-[65px] z-40 w-full border-b transition-colors duration-300 bg-[#0E0F12]/95 border-white/5 data-[theme=light]:bg-[#FAF9F6]/95 data-[theme=light]:border-[#E6E3DD] overflow-x-auto no-scrollbar">
        <div className="max-w-[1440px] mx-auto px-5 md:px-16 py-3 flex items-center gap-2.5 min-w-max">
          {CATEGORIES.map((cat) => {
            const isActive = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? "bg-[#E5A93C] text-black shadow-md shadow-amber-500/20 data-[theme=light]:bg-[#D96B43] data-[theme=light]:text-white data-[theme=light]:shadow-orange-500/20"
                    : "bg-white/5 text-slate-400 border border-white/10 hover:border-white/20 hover:text-white data-[theme=light]:bg-white data-[theme=light]:border-[#E6E3DD] data-[theme=light]:text-stone-600 data-[theme=light]:hover:border-[#D96B43] data-[theme=light]:hover:text-[#D96B43]"
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </div>

      <main className="max-w-[1440px] mx-auto px-5 md:px-16 py-8 space-y-12">
        
        {/* =======================================================================
            3. CURATED SPOTLIGHT HERO SECTION
            ======================================================================= */}
        <section className="relative rounded-2xl overflow-hidden group min-h-[580px] flex items-end border border-white/10 data-[theme=light]:border-[#E6E3DD] shadow-xl">
          {/* Background Exhibition Painting */}
          <div className="absolute inset-0 z-0 overflow-hidden">
            <img
              src={SPOTLIGHT_ARTWORK.image}
              alt={SPOTLIGHT_ARTWORK.title}
              className="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-105 filter brightness-95"
            />
            {/* Vignette Gradients for Legibility in both Light & Dark themes */}
            <div className="absolute inset-0 bg-gradient-to-t from-[#0E0F12] via-[#0E0F12]/60 to-transparent data-[theme=light]:from-[#FAF9F6] data-[theme=light]:via-[#FAF9F6]/50" />
          </div>

          {/* Content Overlay */}
          <div className="relative z-10 w-full p-6 md:p-12 flex flex-col md:flex-row md:items-end justify-between gap-8">
            <div className="max-w-3xl space-y-3.5">
              
              {/* Category & Tags Row */}
              <div className="flex flex-wrap items-center gap-2">
                <span className="px-2.5 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-[#E5A93C]/20 text-[#E5A93C] border border-[#E5A93C]/30 data-[theme=light]:bg-[#D96B43]/15 data-[theme=light]:text-[#D96B43] data-[theme=light]:border-[#D96B43]/30">
                  Spotlight Masterpiece
                </span>
                {SPOTLIGHT_ARTWORK.tags.map((tag) => (
                  <span key={tag} className="text-xs text-slate-300 data-[theme=light]:text-stone-600 font-medium">
                    {tag}
                  </span>
                ))}
              </div>

              {/* Title in Playfair Display */}
              <h1 className="font-serif text-3xl md:text-5xl font-bold tracking-tight text-white data-[theme=light]:text-[#1A1A1E] leading-tight drop-shadow-sm">
                {SPOTLIGHT_ARTWORK.title}
              </h1>

              {/* Description */}
              <p className="text-sm md:text-base text-slate-300 data-[theme=light]:text-stone-700 max-w-2xl leading-relaxed">
                {SPOTLIGHT_ARTWORK.description}
              </p>

              {/* Artist Byline */}
              <div className="flex items-center gap-3.5 pt-2">
                <img
                  src={SPOTLIGHT_ARTWORK.artist.avatar}
                  alt={SPOTLIGHT_ARTWORK.artist.name}
                  className="w-11 h-11 rounded-full border border-white/20 object-cover shadow"
                />
                <div>
                  <p className="text-sm font-semibold text-white data-[theme=light]:text-[#1A1A1E]">
                    {SPOTLIGHT_ARTWORK.artist.name}
                  </p>
                  <p className="text-xs text-slate-400 data-[theme=light]:text-stone-500">
                    {SPOTLIGHT_ARTWORK.artist.title}
                  </p>
                </div>
              </div>
            </div>

            {/* Financial Reservation Box (INR tabular currency contract) */}
            <div className="bg-[#16181F]/80 data-[theme=light]:bg-white/90 backdrop-blur-md p-6 rounded-xl border border-white/10 data-[theme=light]:border-[#E6E3DD] flex flex-col items-start md:items-end shrink-0 shadow-lg">
              <span className="text-[11px] font-bold uppercase tracking-widest text-slate-400 data-[theme=light]:text-stone-500 mb-1">
                Original Valuation
              </span>
              <p className="text-2xl md:text-3xl font-bold font-sans text-[#E5A93C] data-[theme=light]:text-[#D96B43] mb-5 tracking-tight font-mono">
                {SPOTLIGHT_ARTWORK.formattedPrice}
              </p>
              
              <div className="flex flex-col sm:flex-row gap-2.5 w-full">
                <button
                  onClick={() => alert(`Inquiring on commission for "${SPOTLIGHT_ARTWORK.title}" with artist Vikram Adiga.`)}
                  className="bg-[#E5A93C] text-black font-semibold text-xs px-5 py-3 rounded-lg hover:bg-[#F59E0B] data-[theme=light]:bg-[#D96B43] data-[theme=light]:text-white data-[theme=light]:hover:bg-[#BD5630] transition-all shadow-md text-center"
                >
                  Inquire & Commission
                </button>
                <button
                  onClick={() => setActiveModalArtwork(SPOTLIGHT_ARTWORK)}
                  className="bg-white/10 hover:bg-white/20 data-[theme=light]:bg-stone-100 data-[theme=light]:hover:bg-stone-200 text-white data-[theme=light]:text-stone-800 font-semibold text-xs px-5 py-3 rounded-lg border border-white/10 data-[theme=light]:border-stone-300 transition-colors flex items-center justify-center gap-1.5"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 8V4m0 0h4M4 4l5 5m11-1v4m0 0h-4m4 0l-5-5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                  </svg>
                  Full Resolution
                </button>
              </div>
            </div>

          </div>
        </section>

        {/* =======================================================================
            4. CURATED DISCOVERIES HEADER & VIEW SWITCHER
            ======================================================================= */}
        <div className="flex justify-between items-end pt-4 border-b border-white/5 data-[theme=light]:border-[#E6E3DD] pb-4">
          <div>
            <h2 className="font-serif text-2xl md:text-3xl font-semibold text-white data-[theme=light]:text-[#1A1A1E]">
              Curated Discoveries
            </h2>
            <p className="text-xs md:text-sm text-slate-400 data-[theme=light]:text-stone-500 mt-0.5">
              Showing {filteredArtworks.length} authenticated works across traditional and digital mediums
            </p>
          </div>

          <div className="flex items-center gap-1.5">
            <button
              onClick={() => setViewMode("grid")}
              className={`p-2 rounded-lg border transition-colors ${
                viewMode === "grid"
                  ? "bg-white/15 text-[#E5A93C] border-white/20 data-[theme=light]:bg-stone-200 data-[theme=light]:text-[#D96B43] data-[theme=light]:border-stone-300"
                  : "text-slate-400 border-transparent hover:text-white data-[theme=light]:text-stone-400 data-[theme=light]:hover:text-stone-800"
              }`}
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode("list")}
              className={`p-2 rounded-lg border transition-colors ${
                viewMode === "list"
                  ? "bg-white/15 text-[#E5A93C] border-white/20 data-[theme=light]:bg-stone-200 data-[theme=light]:text-[#D96B43] data-[theme=light]:border-stone-300"
                  : "text-slate-400 border-transparent hover:text-white data-[theme=light]:text-stone-400 data-[theme=light]:hover:text-stone-800"
              }`}
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>

        {/* =======================================================================
            5. DYNAMIC MASONRY DISCOVERY GRID
            ======================================================================= */}
        {filteredArtworks.length === 0 ? (
          <div className="text-center py-16 bg-white/5 data-[theme=light]:bg-white rounded-xl border border-white/10 data-[theme=light]:border-[#E6E3DD]">
            <p className="text-lg font-semibold text-slate-300 data-[theme=light]:text-stone-700">No artworks found in this category.</p>
            <p className="text-sm text-slate-400 data-[theme=light]:text-stone-500 mt-1">Try resetting the filter to "All Works" or clear your search term.</p>
            <button
              onClick={() => { setSelectedCategory("All Works"); setSearchQuery(""); }}
              className="mt-4 px-4 py-2 rounded-full text-xs font-semibold bg-[#E5A93C] text-black data-[theme=light]:bg-[#D96B43] data-[theme=light]:text-white"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className={viewMode === "grid" ? "columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6" : "grid grid-cols-1 md:grid-cols-2 gap-6"}>
            {filteredArtworks.map((art) => {
              const userLiked = likedArtworks[art.id]?.liked;
              const likeCount = likedArtworks[art.id]?.count ?? art.likes;

              return (
                <div
                  key={art.id}
                  className="break-inside-avoid relative group rounded-xl overflow-hidden bg-[#16181F] data-[theme=light]:bg-white border border-white/10 data-[theme=light]:border-[#E6E3DD] shadow-md hover:shadow-xl hover:border-[#E5A93C]/40 data-[theme=light]:hover:border-[#D96B43]/50 transition-all duration-300 cursor-pointer"
                  onClick={() => setActiveModalArtwork(art)}
                >
                  {/* Artwork Image */}
                  <div className="relative overflow-hidden bg-black/40">
                    <img
                      src={art.image}
                      alt={art.title}
                      loading="lazy"
                      className="w-full h-auto object-cover transition-transform duration-700 group-hover:scale-105"
                    />

                    {/* Top Badges (Medium & Like trigger) */}
                    <div className="absolute top-3 inset-x-3 flex items-center justify-between pointer-events-none">
                      <span className="px-2.5 py-1 rounded-full text-[11px] font-semibold bg-black/60 backdrop-blur-md text-white border border-white/15">
                        {art.medium}
                      </span>
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleLike(art.id, art.likes);
                        }}
                        className={`pointer-events-auto w-8 h-8 rounded-full flex items-center justify-center backdrop-blur-md border transition-colors ${
                          userLiked
                            ? "bg-rose-500 text-white border-rose-400 shadow-md"
                            : "bg-black/60 text-white border-white/15 hover:text-rose-400"
                        }`}
                      >
                        <svg className="w-4 h-4" fill={userLiked ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  {/* Card Metadata Body */}
                  <div className="p-4 space-y-2.5">
                    <div className="flex items-baseline justify-between gap-2">
                      <h3 className="font-serif text-lg font-semibold text-white data-[theme=light]:text-[#1A1A1E] truncate">
                        {art.title}
                      </h3>
                      <span className="text-sm font-bold text-[#E5A93C] data-[theme=light]:text-[#D96B43] font-mono tabular-nums shrink-0">
                        ₹ {art.priceINR.toLocaleString("en-IN")}
                      </span>
                    </div>

                    {/* Artist Avatar & Byline */}
                    <div className="flex items-center justify-between text-xs text-slate-400 data-[theme=light]:text-stone-500">
                      <div className="flex items-center gap-2">
                        <img
                          src={art.artistAvatar}
                          alt={art.artist}
                          className="w-5 h-5 rounded-full object-cover border border-white/10"
                        />
                        <span className="font-medium text-slate-300 data-[theme=light]:text-stone-700 truncate max-w-[140px]">
                          {art.artist}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-[11px]">
                        <span>👁 {art.views}</span>
                        <span>❤️ {likeCount}</span>
                      </div>
                    </div>

                    {/* Artwork Tags */}
                    <div className="pt-2 border-t border-white/5 data-[theme=light]:border-stone-100 flex flex-wrap gap-1.5">
                      {art.tags.map((tag) => (
                        <span
                          key={tag}
                          className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-white/5 data-[theme=light]:bg-stone-100 text-slate-400 data-[theme=light]:text-stone-600"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>

                </div>
              );
            })}
          </div>
        )}

        {/* =======================================================================
            6. OPEN ARTIST STUDIO BANNER
            ======================================================================= */}
        <section className="rounded-2xl p-8 md:p-10 relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-6 border border-[#E5A93C]/30 data-[theme=light]:border-[#D96B43]/30 bg-[#16181F]/75 data-[theme=light]:bg-white backdrop-blur-lg shadow-lg">
          <div className="absolute top-1/2 left-1/4 -translate-y-1/2 w-80 h-80 bg-amber-500/10 data-[theme=light]:bg-orange-500/10 rounded-full blur-[90px] pointer-events-none" />
          
          <div className="relative z-10 max-w-xl space-y-2">
            <h3 className="font-serif text-2xl md:text-3xl font-bold text-white data-[theme=light]:text-[#1A1A1E]">
              Are you an artist or concept creator?
            </h3>
            <p className="text-sm md:text-base text-slate-300 data-[theme=light]:text-stone-600 leading-relaxed">
              Showcase your portfolio in a museum-grade environment, manage custom client commissions with INR payouts, and harness edge AI vision tools.
            </p>
          </div>

          <a
            href="/dashboard"
            className="relative z-10 whitespace-nowrap bg-[#E5A93C] text-black font-semibold text-sm px-7 py-3.5 rounded-xl hover:bg-[#F59E0B] data-[theme=light]:bg-[#D96B43] data-[theme=light]:text-white data-[theme=light]:hover:bg-[#BD5630] transition-all shadow-md flex items-center gap-2 group"
          >
            <svg className="w-4 h-4 transition-transform group-hover:scale-125" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 4v16m8-8H4" />
            </svg>
            Open Artist Studio
          </a>
        </section>

      </main>

      {/* =========================================================================
          7. FULL RESOLUTION ARTWORK MODAL
          ========================================================================= */}
      {activeModalArtwork && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in"
          onClick={() => setActiveModalArtwork(null)}
        >
          <div
            className="relative max-w-4xl w-full bg-[#16181F] data-[theme=light]:bg-white border border-white/10 data-[theme=light]:border-[#E6E3DD] rounded-2xl overflow-hidden shadow-2xl p-6 md:p-8 space-y-6"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close Button */}
            <button
              onClick={() => setActiveModalArtwork(null)}
              className="absolute top-4 right-4 w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 text-white data-[theme=light]:text-black flex items-center justify-center transition-colors"
            >
              ✕
            </button>

            {/* Modal Image */}
            <div className="w-full max-h-[480px] rounded-xl overflow-hidden bg-black/40 flex items-center justify-center">
              <img
                src={activeModalArtwork.image}
                alt={activeModalArtwork.title}
                className="w-full h-full object-contain max-h-[480px]"
              />
            </div>

            {/* Modal Metadata */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pt-2">
              <div>
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-[#E5A93C]/20 text-[#E5A93C] data-[theme=light]:bg-[#D96B43]/15 data-[theme=light]:text-[#D96B43]">
                  {activeModalArtwork.medium}
                </span>
                <h2 className="font-serif text-2xl font-bold text-white data-[theme=light]:text-[#1A1A1E] mt-1.5">
                  {activeModalArtwork.title}
                </h2>
                <p className="text-xs text-slate-400 data-[theme=light]:text-stone-500">
                  By {typeof activeModalArtwork.artist === "object" ? activeModalArtwork.artist.name : activeModalArtwork.artist}
                </p>
              </div>

              <div className="flex items-center gap-3">
                <span className="text-2xl font-bold text-[#E5A93C] data-[theme=light]:text-[#D96B43] font-mono tabular-nums">
                  ₹ {activeModalArtwork.priceINR?.toLocaleString("en-IN")} INR
                </span>
                <button
                  onClick={() => alert(`Commission request sent for "${activeModalArtwork.title}"!`)}
                  className="bg-[#E5A93C] text-black data-[theme=light]:bg-[#D96B43] data-[theme=light]:text-white px-5 py-2.5 rounded-lg font-semibold text-xs transition-colors shadow"
                >
                  Commission Artwork
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* =========================================================================
          8. FOOTER
          ========================================================================= */}
      <footer className="border-t border-white/5 data-[theme=light]:border-[#E6E3DD] mt-16 py-8 text-center text-xs text-slate-500 data-[theme=light]:text-stone-400">
        <p>© 2026 ArtistryHub Platform. Museum-Grade Digital Art & Creative Studio.</p>
      </footer>

    </div>
  );
}
