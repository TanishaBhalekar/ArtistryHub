import random

STYLE_DATABASE = [
    {
        'id': 'art-nouveau',
        'title': 'Art Nouveau',
        'era': '1890 – 1910',
        'category': 'Classic Masters',
        'description': 'Characterized by organic, sinuous whip-snake curves, intricate floral filigree, and decorative gold foil accents.',
        'masters': 'Alphonse Mucha, Gustav Klimt, Antoni Gaudí',
        'palette': ['#D4AF37', '#2E5B44', '#C85A32', '#F4E8C1', '#1B263B'],
        'prompt_keywords': 'Art Nouveau, Alphonse Mucha style, intricate gold filigree, flowing organic curves, stained glass border, ornate poster art',
        'image': 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=500&q=80'
    },
    {
        'id': 'cyberpunk-synthwave',
        'title': 'Cyberpunk / Synthwave',
        'era': 'Modern Digital',
        'category': 'Modern Digital',
        'description': 'High-tech low-life aesthetic with vibrant neon cyan and magenta rim lighting, rain-slicked reflective surfaces, and retro-futuristic grids.',
        'masters': 'Syd Mead, H.R. Giger, Katsuhiro Otomo',
        'palette': ['#06B6D4', '#EC4899', '#8B5CF6', '#0F172A', '#F43F5E'],
        'prompt_keywords': 'Cyberpunk city, neon cyan magenta rim light, Octane Render 8k, raytraced reflections, futuristic dystopia, high detail',
        'image': 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=500&q=80'
    },
    {
        'id': 'impressionism',
        'title': 'Impressionism',
        'era': '1860s – 1880s',
        'category': 'Classic Masters',
        'description': 'Emphasizes vibrant natural light, visible painterly impasto brushstrokes, and fleeting atmospheric conditions.',
        'masters': 'Claude Monet, Vincent van Gogh, Pierre-Auguste Renoir',
        'palette': ['#3B82F6', '#F59E0B', '#10B981', '#F43F5E', '#FEF08A'],
        'prompt_keywords': 'Impressionist oil painting, thick impasto brushstrokes, Claude Monet light dynamics, vibrant color harmony, plein air',
        'image': 'https://images.unsplash.com/photo-1541701494587-cb58502866ab?auto=format&fit=crop&w=500&q=80'
    },
    {
        'id': 'surrealism',
        'title': 'Surrealism',
        'era': '1920s – 1950s',
        'category': 'Avant-Garde',
        'description': 'Unlocks the subconscious through dreamlike juxtapositions, melting architectural forms, and symbolic imagery.',
        'masters': 'Salvador Dalí, René Magritte, Max Ernst',
        'palette': ['#E11D48', '#0284C7', '#D97706', '#1E293B', '#F8FAFC'],
        'prompt_keywords': 'Surrealist dreamscape, Salvador Dali style, floating impossible architecture, symbolic juxtaposition, hyper-real lighting',
        'image': 'https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?auto=format&fit=crop&w=500&q=80'
    },
    {
        'id': 'chiaroscuro-renaissance',
        'title': 'Renaissance Chiaroscuro',
        'era': '1400s – 1600s',
        'category': 'Classic Masters',
        'description': 'Dramatic contrast between intense directional light and deep impenetrable shadows to create volumetric depth and emotional drama.',
        'masters': 'Caravaggio, Rembrandt, Leonardo da Vinci',
        'palette': ['#78350F', '#B45309', '#172554', '#0F172A', '#FEF3C7'],
        'prompt_keywords': 'Chiaroscuro lighting, Caravaggio master oil painting, dramatic single light source, deep rich shadows, Renaissance portrait',
        'image': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=500&q=80'
    },
    {
        'id': 'ukiyo-e-woodblock',
        'title': 'Ukiyo-e Woodblock',
        'era': '1600s – 1800s',
        'category': 'Asian Art',
        'description': 'Traditional Japanese floating world prints with flat decorative color fields, expressive black ink linework, and wave motifs.',
        'masters': 'Katsushika Hokusai, Utagawa Hiroshige',
        'palette': ['#1E3A8A', '#DC2626', '#EAB308', '#FEF3C7', '#111827'],
        'prompt_keywords': 'Ukiyo-e woodblock print, Hokusai style, Japanese ink linework, flat color planes, traditional woodcut texture',
        'image': 'https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=500&q=80'
    }
]

THEME_TEMPLATES = {
    'Cyberpunk City': 'A sprawling neon-drenched metropolis with rain-slicked asphalt streets and soaring megastructures',
    'Solar Fantasy': 'A celestial solar citadel floating amidst radiant nebula clouds and orbiting golden rings',
    'Underwater Ruins': 'Sunken ancient temple ruins overgrown with bioluminescent coral and glowing deep-sea flora',
    'Victorian Steampunk': 'An ornate Victorian workshop filled with polished brass clockwork gears, copper pipes, and steam vents',
    'Deep Space Odyssey': 'A massive interstellar research station silhouetted against a swirling galaxy event horizon',
    'Mythological Realm': 'An ethereal sacred grove with towering glowing ancient trees and mystical mana streams',
    'Post-Apocalyptic Nature': 'Overgrown glass skyscrapers reclaimed by wild emerald moss and cascading waterfalls'
}

MOOD_MODIFIERS = {
    'Ethereal & Mystical': 'shrouded in glowing ethereal mist and soft ambient energy, evoking a sense of divine mystery and wonder',
    'Dark & Melancholic': 'bathed in deep shadow with atmospheric fog and somber tones, evoking dramatic tension and melancholy',
    'Vibrant & Energetic': 'bursting with vivid high-contrast colors, dynamic motion trails, and electric radiance',
    'Serene & Peaceful': 'illuminated by gentle harmonic light, serene reflections, and tranquil natural balance',
    'Tense & Chaotic': 'charged with volatile atmospheric energy, swirling embers, and dramatic high-contrast action'
}

STYLE_DIRECTIVES = {
    'Digital Concept Art (UE5)': 'masterpiece digital concept art, Octane Render 8K, Unreal Engine 5 render, trending on ArtStation',
    'Oil Painting (Impressionism)': 'fine art oil painting, visible impasto brushstrokes, rich color blending, museum gallery quality',
    'Anime / Cel-Shaded': 'vibrant anime key visual, clean expressive linework, dynamic cel-shading, Ufotable aesthetic',
    'Watercolor & Ink': 'expressive watercolor wash on cold-press paper, delicate black ink contour lines, fluid pigment bleeds',
    'Octane Render 3D': 'hyper-realistic 3D render, volumetric lighting, photorealistic subsurface scattering, raytraced shadows',
    'Renaissance Chiaroscuro': 'dramatic Caravaggio chiaroscuro oil painting, high contrast single light source, classical masterpiece'
}

LIGHTING_DIRECTIVES = {
    'Volumetric Sunbeams': 'crepuscular sunbeams breaking through atmospheric haze',
    'Neon Rim Lighting': 'dramatic cyan and magenta dual rim lighting',
    'Cinematic Wide Angle': 'dramatic golden hour sunlight casting long shadows',
    'Biomagnetic Glow': 'bioluminescent soft ambient luminescence',
    'Studio Softbox': 'soft studio key lighting with gentle fill shadows'
}

CAMERA_DIRECTIVES = {
    'Cinematic Wide Angle': 'shot on 24mm anamorphic lens, wide cinematic aspect ratio',
    'Macro Detail': 'extreme macro close-up, shallow depth of field, crisp focal point',
    'Bird Eye View': 'dramatic aerial bird-eye perspective, sweeping focal depth',
    'Low Angle Hero': 'low angle dramatic perspective, imposing scale and depth'
}

def construct_prompt(theme='Cyberpunk City', mood='Ethereal & Mystical', style='Digital Concept Art (UE5)', lighting='Neon Rim Lighting', camera='Cinematic Wide Angle'):
    """
    Mathematically constructs a detailed descriptive AI prompt from modular parameters.
    """
    base_theme = THEME_TEMPLATES.get(theme, THEME_TEMPLATES['Cyberpunk City'])
    base_mood = MOOD_MODIFIERS.get(mood, MOOD_MODIFIERS['Ethereal & Mystical'])
    base_style = STYLE_DIRECTIVES.get(style, STYLE_DIRECTIVES['Digital Concept Art (UE5)'])
    base_lighting = LIGHTING_DIRECTIVES.get(lighting, LIGHTING_DIRECTIVES['Neon Rim Lighting'])
    base_camera = CAMERA_DIRECTIVES.get(camera, CAMERA_DIRECTIVES['Cinematic Wide Angle'])

    # Assemble main prompt
    main_prompt = f"{base_theme}, {base_mood}. {base_lighting}, {base_camera}. {base_style}, intricate details, highly detailed, 8k resolution."
    
    negative_prompt = "blurry, low quality, distorted proportions, watermarks, signature, oversaturated artifacts, out of frame"

    tags = [theme, mood, style, lighting, camera]

    return {
        'prompt': main_prompt,
        'negative_prompt': negative_prompt,
        'theme': theme,
        'mood': mood,
        'style': style,
        'lighting': lighting,
        'camera': camera,
        'tags': tags,
        'seed': random.randint(100000, 999999)
    }
