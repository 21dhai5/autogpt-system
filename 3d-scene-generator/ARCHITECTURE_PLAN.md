# 3D Scene Generator MVP Architecture

## Goals
- Input a scene description
- Generate multiple view images via AI image API
- Derive approximate depth for each view and reconstruct a lightweight 3D point cloud / billboard scene
- View the reconstructed scene in browser with free camera controls
- Save and reload generated scenes

## MVP Decisions
- Backend: FastAPI for API + static file serving
- Storage: JSON scene records on disk under `workspace/data/scenes`, SQLite can be added later
- AI image generation: pluggable provider interface; default mock generator for offline/demo operation, optional OpenAI-compatible image API via environment variables
- Reconstruction: estimate pseudo-depth from luminance/gradients if no ML depth model is available, then fuse samples from each camera into a colored point cloud and textured camera billboards
- Frontend: vanilla HTML/CSS/JS with Three.js from CDN, OrbitControls for rotate/pan/zoom, responsive layout
- Export: MVP includes JSON export and viewport image export; placeholders for future video/mesh export documented in README

## Backend Endpoints
- `POST /api/scenes/generate` create a new scene from prompt
- `GET /api/scenes` list saved scenes
- `GET /api/scenes/{scene_id}` get scene payload
- `GET /api/health` health check

## Scene Generation Flow
1. Receive prompt from frontend
2. Generate 4 views: front, left, right, overhead using provider
3. Save images under `data/generated/{scene_id}`
4. Compute depth map per image
5. Back-project sampled pixels to 3D points using predefined camera poses
6. Save scene JSON with camera metadata, images, depth maps, and point cloud
7. Frontend loads scene JSON and renders points + camera planes

## File Plan
- `workspace/app/main.py` FastAPI app and routes
- `workspace/app/models.py` pydantic models
- `workspace/app/services/generator.py` image provider abstraction
- `workspace/app/services/reconstruction.py` image/depth/point-cloud logic
- `workspace/app/services/storage.py` persistence helpers
- `workspace/frontend/index.html`, `styles.css`, `app.js`
- `workspace/README.md`, `workspace/docs/API.md`, `workspace/docs/ARCHITECTURE.md`
