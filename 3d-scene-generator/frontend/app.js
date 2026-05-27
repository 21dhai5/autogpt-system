import * as THREE from 'https://unpkg.com/three@0.165.0/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.165.0/examples/jsm/controls/OrbitControls.js';

const state = {
  currentScene: null,
  renderer: null,
  camera: null,
  scene: null,
  controls: null,
  mesh: null,
  frameId: null,
};

const els = {
  form: document.getElementById('scene-form'),
  prompt: document.getElementById('prompt'),
  style: document.getElementById('style'),
  resolution: document.getElementById('resolution'),
  generateBtn: document.getElementById('generate-btn'),
  sampleBtn: document.getElementById('sample-btn'),
  refreshScenes: document.getElementById('refresh-scenes'),
  sceneList: document.getElementById('scene-list'),
  sceneTitle: document.getElementById('scene-title'),
  sceneMeta: document.getElementById('scene-meta'),
  statusBadge: document.getElementById('status-badge'),
  viewerContainer: document.getElementById('viewer-container'),
  viewsGrid: document.getElementById('views-grid'),
  stats: document.getElementById('reconstruction-stats'),
  exportJson: document.getElementById('export-json'),
  exportPly: document.getElementById('export-ply'),
  captureImage: document.getElementById('capture-image'),
};

init();

async function init() {
  setupViewer();
  bindEvents();
  await loadSavedScenes();
  await loadSamplePrompt();
}

function bindEvents() {
  els.form.addEventListener('submit', onGenerate);
  els.sampleBtn.addEventListener('click', loadSamplePrompt);
  els.refreshScenes.addEventListener('click', loadSavedScenes);
  els.exportJson.addEventListener('click', () => exportScene('json'));
  els.exportPly.addEventListener('click', () => exportScene('ply'));
  els.captureImage.addEventListener('click', captureImage);
  window.addEventListener('resize', onResize);
}

async function onGenerate(event) {
  event.preventDefault();
  const prompt = els.prompt.value.trim();
  if (!prompt) return;

  setStatus('正在生成多视角图像与 3D 场景...', 'busy');
  els.generateBtn.disabled = true;

  try {
    const response = await fetch('/api/scenes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt,
        style: els.style.value,
        resolution: Number(els.resolution.value),
      }),
    });

    if (!response.ok) throw new Error('场景生成失败');
    const scene = await response.json();
    renderScene(scene);
    await loadSavedScenes();
    setStatus('场景生成完成', 'success');
  } catch (error) {
    console.error(error);
    setStatus(error.message || '生成失败', 'error');
  } finally {
    els.generateBtn.disabled = false;
  }
}

async function loadSavedScenes() {
  const response = await fetch('/api/scenes');
  const data = await response.json();
  els.sceneList.innerHTML = '';

  if (!data.items.length) {
    els.sceneList.innerHTML = '<p class="hint">暂无场景，先生成一个试试。</p>';
    return;
  }

  data.items.forEach((item) => {
    const button = document.createElement('button');
    button.className = 'scene-item';
    button.innerHTML = `
      <img src="${item.preview_url}" alt="${item.title}" />
      <div>
        <h4>${item.title}</h4>
        <p>${item.prompt}</p>
      </div>
    `;
    button.addEventListener('click', async () => {
      const response = await fetch(`/api/scenes/${item.id}`);
      const scene = await response.json();
      renderScene(scene);
      setStatus('已加载历史场景', 'success');
    });
    els.sceneList.appendChild(button);
  });
}

async function loadSamplePrompt() {
  try {
    const response = await fetch('/api/demo/prompt-samples');
    const data = await response.json();
    if (data.items?.length) {
      els.prompt.value = data.items[Math.floor(Math.random() * data.items.length)];
    }
  } catch (error) {
    console.warn('加载示例提示词失败', error);
  }
}

function setupViewer() {
  const width = els.viewerContainer.clientWidth || 900;
  const height = els.viewerContainer.clientHeight || 560;

  state.scene = new THREE.Scene();
  state.scene.background = new THREE.Color(0x09111f);
  state.scene.fog = new THREE.Fog(0x09111f, 14, 28);

  state.camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 100);
  state.camera.position.set(8, 7, 8);

  state.renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  state.renderer.setPixelRatio(window.devicePixelRatio);
  state.renderer.setSize(width, height);
  els.viewerContainer.appendChild(state.renderer.domElement);

  state.controls = new OrbitControls(state.camera, state.renderer.domElement);
  state.controls.enableDamping = true;
  state.controls.target.set(0, 0.4, 0);

  const hemi = new THREE.HemisphereLight(0xdbeafe, 0x0b1120, 1.4);
  const dir = new THREE.DirectionalLight(0xffffff, 1.1);
  dir.position.set(6, 8, 4);

  const grid = new THREE.GridHelper(18, 18, 0x334155, 0x1e293b);
  grid.position.y = -1.25;

  state.scene.add(hemi, dir, grid);
  animate();
}

function renderScene(scenePayload) {
  state.currentScene = scenePayload;
  els.sceneTitle.textContent = scenePayload.title;
  els.sceneMeta.textContent = `${scenePayload.prompt} · ${scenePayload.style} · ${scenePayload.resolution}px`;

  updateViews(scenePayload.reconstruction.views);
  updateStats(scenePayload.reconstruction);
  updateExports(scenePayload);
  drawMesh(scenePayload.reconstruction.mesh, scenePayload.camera);
}

function drawMesh(meshData, cameraState) {
  if (state.mesh) {
    state.scene.remove(state.mesh);
    state.mesh.geometry.dispose();
    state.mesh.material.dispose();
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(meshData.vertices, 3));
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(meshData.colors, 3));
  geometry.setIndex(meshData.indices.flat());
  geometry.computeVertexNormals();

  const material = new THREE.MeshStandardMaterial({
    vertexColors: true,
    metalness: 0.05,
    roughness: 0.9,
    flatShading: false,
  });

  state.mesh = new THREE.Mesh(geometry, material);
  state.scene.add(state.mesh);

  if (cameraState?.position && cameraState?.target) {
    state.camera.position.set(cameraState.position.x, cameraState.position.y, cameraState.position.z);
    state.controls.target.set(cameraState.target.x, cameraState.target.y, cameraState.target.z);
    state.controls.update();
  }
}

function updateViews(views) {
  els.viewsGrid.innerHTML = '';
  views.forEach((view) => {
    const article = document.createElement('article');
    article.className = 'view-card';
    article.innerHTML = `
      <img src="${view.image_url}" alt="${view.label}" />
      <span>${view.label}</span>
    `;
    els.viewsGrid.appendChild(article);
  });
}

function updateStats(reconstruction) {
  const stats = [
    ['重建类型', reconstruction.type],
    ['采样点数量', reconstruction.point_count.toLocaleString()],
    ['网格分辨率', `${reconstruction.mesh.grid} x ${reconstruction.mesh.grid}`],
    ['视角数量', reconstruction.views.length],
  ];
  els.stats.innerHTML = stats
    .map(([label, value]) => `<div><dt>${label}</dt><dd>${value}</dd></div>`)
    .join('');
}

function updateExports(scenePayload) {
  els.exportJson.disabled = false;
  els.exportPly.disabled = false;
  els.captureImage.disabled = false;
  els.exportJson.dataset.url = scenePayload.exports.json;
  els.exportPly.dataset.url = scenePayload.exports.ply;
}

function exportScene(format) {
  const url = format === 'json' ? els.exportJson.dataset.url : els.exportPly.dataset.url;
  if (url) window.open(url, '_blank');
}

function captureImage() {
  if (!state.renderer) return;
  const link = document.createElement('a');
  link.href = state.renderer.domElement.toDataURL('image/png');
  link.download = `${state.currentScene?.id || 'scene'}-capture.png`;
  link.click();
}

function onResize() {
  if (!state.renderer || !state.camera) return;
  const width = els.viewerContainer.clientWidth || 900;
  const height = els.viewerContainer.clientHeight || 560;
  state.camera.aspect = width / height;
  state.camera.updateProjectionMatrix();
  state.renderer.setSize(width, height);
}

function animate() {
  state.frameId = requestAnimationFrame(animate);
  state.controls?.update();
  state.renderer?.render(state.scene, state.camera);
}

function setStatus(text, type) {
  els.statusBadge.textContent = text;
  const colors = {
    busy: 'rgba(56, 189, 248, 0.18)',
    success: 'rgba(16, 185, 129, 0.16)',
    error: 'rgba(249, 115, 22, 0.16)',
  };
  const textColors = {
    busy: '#7dd3fc',
    success: '#a7f3d0',
    error: '#fdba74',
  };
  els.statusBadge.style.background = colors[type] || colors.success;
  els.statusBadge.style.color = textColors[type] || textColors.success;
}
