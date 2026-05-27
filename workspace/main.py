from pathlib import Path
import json
import math
import os
import random
import textwrap
import uuid
from datetime import datetime
from typing import Dict, List, Literal, Optional

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "scenes"
STATIC_DIR = BASE_DIR / "frontend"
EXPORT_DIR_NAME = "exports"
IMAGES_DIR_NAME = "images"

app = FastAPI(title="AI 3D Scene Generator MVP", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR.mkdir(parents=True, exist_ok=True)


class SceneGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=500)
    style: str = Field(default="cinematic")
    resolution: int = Field(default=512, ge=256, le=1024)


class ExportRequest(BaseModel):
    format: Literal["json", "ply"]


class CameraState(BaseModel):
    position: Dict[str, float]
    target: Dict[str, float]


class SceneUpdateRequest(BaseModel):
    title: Optional[str] = None
    camera: Optional[CameraState] = None


VIEW_SPECS = [
    {"id": "front", "yaw": 0, "pitch": 0, "label": "Front View"},
    {"id": "left", "yaw": -90, "pitch": 0, "label": "Left View"},
    {"id": "right", "yaw": 90, "pitch": 0, "label": "Right View"},
    {"id": "top", "yaw": 0, "pitch": -65, "label": "Top View"},
]


class MockImageGenerator:
    def generate_views(self, prompt: str, resolution: int, output_dir: Path) -> List[Dict]:
        seed = abs(hash(prompt)) % (2**32)
        output_dir.mkdir(parents=True, exist_ok=True)
        views = []
        for index, view in enumerate(VIEW_SPECS):
            image = self._render_prompt(prompt, resolution, view, seed + index)
            filename = f"{view['id']}.png"
            filepath = output_dir / filename
            image.save(filepath)
            views.append(
                {
                    "id": view["id"],
                    "label": view["label"],
                    "yaw": view["yaw"],
                    "pitch": view["pitch"],
                    "image_url": f"/data/scenes/{output_dir.parent.name}/{IMAGES_DIR_NAME}/{filename}",
                    "filename": filename,
                }
            )
        return views

    def _render_prompt(self, prompt: str, resolution: int, view: Dict, seed: int) -> Image.Image:
        rng = random.Random(seed)
        image = Image.new("RGB", (resolution, resolution), self._pick_palette(prompt, rng)[0])
        draw = ImageDraw.Draw(image)
        palette = self._pick_palette(prompt, rng)

        for y in range(resolution):
            ratio = y / max(1, resolution - 1)
            r = int(palette[0][0] * (1 - ratio) + palette[1][0] * ratio)
            g = int(palette[0][1] * (1 - ratio) + palette[1][1] * ratio)
            b = int(palette[0][2] * (1 - ratio) + palette[1][2] * ratio)
            draw.line((0, y, resolution, y), fill=(r, g, b))

        horizon = int(resolution * 0.58)
        draw.rectangle((0, horizon, resolution, resolution), fill=palette[2])

        for _ in range(6):
            cx = rng.randint(0, resolution)
            cy = rng.randint(0, int(resolution * 0.35))
            radius = rng.randint(resolution // 18, resolution // 8)
            draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(255, 255, 255, 90))

        offset = view["yaw"] / 90.0
        center_x = resolution * (0.5 + offset * 0.12)
        width = resolution * (0.22 + abs(offset) * 0.02)
        height = resolution * (0.26 - abs(offset) * 0.015)
        base_y = horizon + resolution * 0.03

        draw.polygon(
            [
                (center_x - width * 0.6, base_y),
                (center_x, base_y - height),
                (center_x + width * 0.6, base_y),
                (center_x + width * 0.4, base_y + height * 0.95),
                (center_x - width * 0.4, base_y + height * 0.95),
            ],
            fill=palette[3],
        )

        if "city" in prompt.lower() or "building" in prompt.lower():
            for i in range(5):
                bw = resolution * (0.08 + i * 0.01)
                bh = resolution * (0.14 + i * 0.05)
                bx = resolution * 0.15 + i * resolution * 0.13 + offset * 12
                by = horizon - bh
                draw.rectangle((bx, by, bx + bw, horizon), fill=palette[4])
                for row in range(4):
                    for col in range(2):
                        wx = bx + 10 + col * (bw / 2.5)
                        wy = by + 10 + row * (bh / 5)
                        draw.rectangle((wx, wy, wx + 8, wy + 12), fill=(255, 236, 140))
        else:
            for i in range(7):
                tx = resolution * 0.1 + i * resolution * 0.12 + offset * 8
                th = resolution * (0.12 + rng.random() * 0.1)
                draw.rectangle((tx, horizon - th * 0.2, tx + 8, horizon + th * 0.35), fill=(90, 60, 35))
                draw.ellipse((tx - 22, horizon - th, tx + 30, horizon - 10), fill=palette[4])

        wrapped = textwrap.fill(prompt[:90], width=22)
        draw.rounded_rectangle((18, 18, resolution - 18, 110), radius=18, fill=(0, 0, 0))
        draw.text((34, 30), f"{view['label']}\n{wrapped}", fill=(255, 255, 255))
        return image.filter(ImageFilter.GaussianBlur(radius=0.3))

    def _pick_palette(self, prompt: str, rng: random.Random):
        prompt_lower = prompt.lower()
        if "desert" in prompt_lower:
            return [(245, 190, 110), (255, 140, 100), (205, 150, 90), (140, 90, 60), (120, 130, 70)]
        if "snow" in prompt_lower or "ice" in prompt_lower:
            return [(180, 220, 255), (220, 245, 255), (235, 240, 245), (170, 180, 200), (110, 150, 180)]
        if "forest" in prompt_lower:
            return [(80, 145, 110), (170, 210, 180), (105, 140, 85), (130, 90, 75), (50, 110, 60)]
        if "night" in prompt_lower:
            return [(30, 40, 85), (100, 80, 150), (40, 50, 70), (190, 120, 210), (80, 90, 120)]
        base = [
            [(88, 165, 220), (215, 235, 252), (105, 155, 95), (180, 120, 95), (75, 120, 80)],
            [(120, 110, 200), (255, 188, 126), (95, 122, 88), (155, 102, 78), (84, 96, 132)],
        ]
        return rng.choice(base)


class DepthReconstructor:
    def reconstruct(self, scene_id: str, prompt: str, resolution: int, views: List[Dict]) -> Dict:
        prompt_factor = 0.9 + (len(prompt) % 9) / 10
        grid = 40
        points = []
        vertices = []
        colors = []
        for zi in range(grid):
            for xi in range(grid):
                nx = xi / (grid - 1)
                nz = zi / (grid - 1)
                x = (nx - 0.5) * 14
                z = (nz - 0.5) * 14
                y = self._height(x, z, prompt_factor)
                color = self._color_from_height(y, prompt)
                vertices.extend([round(x, 4), round(y, 4), round(z, 4)])
                colors.extend(color)
                points.append({"x": round(x, 4), "y": round(y, 4), "z": round(z, 4), "color": color})

        quads = []
        for zi in range(grid - 1):
            for xi in range(grid - 1):
                a = zi * grid + xi
                b = a + 1
                c = a + grid
                d = c + 1
                quads.append([a, c, b])
                quads.append([b, c, d])

        camera_presets = [
            {"name": "overview", "position": {"x": 8, "y": 7, "z": 8}, "target": {"x": 0, "y": 0, "z": 0}},
            {"name": "low-angle", "position": {"x": 0, "y": 2.5, "z": 11}, "target": {"x": 0, "y": 1, "z": 0}},
        ]

        return {
            "scene_id": scene_id,
            "type": "heightfield",
            "resolution": resolution,
            "views": views,
            "point_count": len(points),
            "mesh": {"vertices": vertices, "indices": quads, "colors": colors, "grid": grid},
            "point_cloud": points[::6],
            "camera_presets": camera_presets,
            "bounds": {"min": {"x": -7, "y": -1.2, "z": -7}, "max": {"x": 7, "y": 3.8, "z": 7}},
        }

    def _height(self, x: float, z: float, factor: float) -> float:
        ridge = math.sin(x * 0.55) * 0.9 + math.cos(z * 0.45) * 0.7
        ripple = math.sin((x + z) * 0.9) * 0.22
        mound = math.exp(-0.04 * (x * x + z * z)) * 2.2
        return round((ridge + ripple + mound - 0.9) * factor, 4)

    def _color_from_height(self, height: float, prompt: str) -> List[float]:
        if "snow" in prompt.lower():
            return [0.85, 0.9, 0.96] if height > 0.8 else [0.6, 0.72, 0.78]
        if "desert" in prompt.lower():
            return [0.82, 0.66, 0.4] if height > 0.5 else [0.72, 0.56, 0.3]
        if height > 1.4:
            return [0.78, 0.78, 0.8]
        if height > 0.2:
            return [0.32, 0.62, 0.35]
        return [0.22, 0.42, 0.24]


image_generator = MockImageGenerator()
reconstructor = DepthReconstructor()


def scene_dir(scene_id: str) -> Path:
    return DATA_DIR / scene_id


def scene_file(scene_id: str) -> Path:
    return scene_dir(scene_id) / "scene.json"


def ensure_scene(scene_id: str) -> Dict:
    path = scene_file(scene_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Scene not found")
    return json.loads(path.read_text(encoding="utf-8"))


def save_scene(payload: Dict) -> None:
    directory = scene_dir(payload["id"])
    directory.mkdir(parents=True, exist_ok=True)
    (directory / EXPORT_DIR_NAME).mkdir(parents=True, exist_ok=True)
    scene_file(payload["id"]).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_scene_payload(prompt: str, style: str, resolution: int) -> Dict:
    scene_id = uuid.uuid4().hex[:12]
    created_at = datetime.utcnow().isoformat() + "Z"
    directory = scene_dir(scene_id)
    views = image_generator.generate_views(prompt, resolution, directory / IMAGES_DIR_NAME)
    reconstruction = reconstructor.reconstruct(scene_id, prompt, resolution, views)
    preview_path = directory / "preview.png"
    Image.open(directory / IMAGES_DIR_NAME / "front.png").save(preview_path)
    return {
        "id": scene_id,
        "title": prompt[:48],
        "prompt": prompt,
        "style": style,
        "resolution": resolution,
        "created_at": created_at,
        "updated_at": created_at,
        "preview_url": f"/data/scenes/{scene_id}/preview.png",
        "reconstruction": reconstruction,
        "camera": {"position": {"x": 8, "y": 7, "z": 8}, "target": {"x": 0, "y": 0.5, "z": 0}},
        "exports": {
            "json": f"/api/scenes/{scene_id}/export/json",
            "ply": f"/api/scenes/{scene_id}/export/ply",
        },
    }


def to_summary(scene: Dict) -> Dict:
    return {
        "id": scene["id"],
        "title": scene.get("title") or scene["prompt"][:40],
        "prompt": scene["prompt"],
        "style": scene.get("style", "cinematic"),
        "created_at": scene["created_at"],
        "updated_at": scene.get("updated_at", scene["created_at"]),
        "preview_url": scene.get("preview_url"),
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "scene_count": len(list(DATA_DIR.glob("*/scene.json")))}


@app.post("/api/scenes")
def create_scene(payload: SceneGenerateRequest):
    scene = build_scene_payload(payload.prompt, payload.style, payload.resolution)
    save_scene(scene)
    return scene


@app.get("/api/scenes")
def list_scenes():
    scenes = []
    for path in sorted(DATA_DIR.glob("*/scene.json"), reverse=True):
        scenes.append(to_summary(json.loads(path.read_text(encoding="utf-8"))))
    return {"items": scenes}


@app.get("/api/scenes/{scene_id}")
def get_scene(scene_id: str):
    return ensure_scene(scene_id)


@app.put("/api/scenes/{scene_id}")
def update_scene(scene_id: str, payload: SceneUpdateRequest):
    scene = ensure_scene(scene_id)
    if payload.title is not None:
        scene["title"] = payload.title
    if payload.camera is not None:
        scene["camera"] = payload.camera.model_dump()
    scene["updated_at"] = datetime.utcnow().isoformat() + "Z"
    save_scene(scene)
    return scene


@app.get("/api/scenes/{scene_id}/export/{fmt}")
def export_scene(scene_id: str, fmt: str):
    scene = ensure_scene(scene_id)
    export_dir = scene_dir(scene_id) / EXPORT_DIR_NAME
    export_dir.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        target = export_dir / f"{scene_id}.json"
        target.write_text(json.dumps(scene["reconstruction"], ensure_ascii=False, indent=2), encoding="utf-8")
        return FileResponse(target, media_type="application/json", filename=target.name)
    if fmt == "ply":
        target = export_dir / f"{scene_id}.ply"
        write_ply(target, scene["reconstruction"]["point_cloud"])
        return FileResponse(target, media_type="application/octet-stream", filename=target.name)
    raise HTTPException(status_code=400, detail="Unsupported export format")


@app.get("/api/demo/prompt-samples")
def prompt_samples():
    return {
        "items": [
            "A futuristic mountain observatory at sunrise",
            "A tranquil forest shrine with mist and lanterns",
            "A desert canyon research base at golden hour",
            "A floating island city above the clouds at night",
        ]
    }


def write_ply(target: Path, points: List[Dict]) -> None:
    lines = [
        "ply",
        "format ascii 1.0",
        f"element vertex {len(points)}",
        "property float x",
        "property float y",
        "property float z",
        "property uchar red",
        "property uchar green",
        "property uchar blue",
        "end_header",
    ]
    for point in points:
        red, green, blue = [max(0, min(255, int(channel * 255))) for channel in point["color"]]
        lines.append(f"{point['x']} {point['y']} {point['z']} {red} {green} {blue}")
    target.write_text("\n".join(lines), encoding="utf-8")


app.mount("/data", StaticFiles(directory=BASE_DIR / "data"), name="data")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)
