const THREE_URL = "./vendor/three.module.js";

const defaults = {
    speed: 1,
    pointSize: 0.08,
    opacity: 0.4,
    maskStart: 0.2,
    maskSolid: 0.5,
};

async function mountStructureFlow(host) {
    if (!host || host.dataset.mounted === "true") return;
    host.dataset.mounted = "true";

    let THREE;
    try {
        THREE = await import(THREE_URL);
    } catch (error) {
        host.classList.add("structure-flow-unavailable");
        console.warn("Structure Flow could not load Three.js", error);
        return;
    }

    const settings = {
        speed: Number(host.dataset.speed ?? defaults.speed),
        pointSize: Number(host.dataset.pointSize ?? defaults.pointSize),
        opacity: Number(host.dataset.opacity ?? defaults.opacity),
        maskStart: Number(host.dataset.maskStart ?? defaults.maskStart),
        maskSolid: Number(host.dataset.maskSolid ?? defaults.maskSolid),
    };
    const mask = `linear-gradient(to bottom, transparent ${settings.maskStart * 100}%, black ${settings.maskSolid * 100}%, black 100%)`;
    host.style.maskImage = mask;
    host.style.webkitMaskImage = mask;

    const canvas = document.createElement("canvas");
    canvas.setAttribute("aria-hidden", "true");
    host.appendChild(canvas);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
    camera.position.z = 30;
    camera.position.y = 5;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    const geometry = new THREE.BufferGeometry();
    const pointCount = 15000;
    const positions = new Float32Array(pointCount * 3);
    const radius = 25;
    for (let index = 0; index < pointCount; index += 1) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(Math.random() * 0.8 + 0.2);
        positions[index * 3] = radius * Math.sin(phi) * Math.cos(theta);
        positions[index * 3 + 1] = radius * Math.cos(phi) - 20;
        positions[index * 3 + 2] = radius * Math.sin(phi) * Math.sin(theta);
    }
    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
        size: settings.pointSize,
        color: 0xffffff,
        transparent: true,
        opacity: settings.opacity,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
    });
    const points = new THREE.Points(geometry, material);
    scene.add(points);

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    let visible = !document.hidden;
    let intersecting = true;
    let contextLost = false;
    let frame = 0;

    const resize = () => {
        const bounds = host.getBoundingClientRect();
        const width = Math.max(1, bounds.width);
        const height = Math.max(1, bounds.height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, width < 700 ? 1.5 : 2));
        renderer.setSize(width, height, false);
        render();
    };

    const render = () => {
        points.rotation.y += reducedMotion.matches ? 0 : 0.0008 * settings.speed;
        points.rotation.z += reducedMotion.matches ? 0 : 0.0002 * settings.speed;
        material.size = settings.pointSize;
        material.opacity = settings.opacity;
        renderer.render(scene, camera);
    };
    const tick = () => {
        frame = 0;
        if (!visible || !intersecting || contextLost) return;
        render();
        if (!reducedMotion.matches) frame = requestAnimationFrame(tick);
    };
    const start = () => {
        if (!frame && visible && intersecting && !contextLost) frame = requestAnimationFrame(tick);
    };
    const stop = () => {
        if (frame) cancelAnimationFrame(frame);
        frame = 0;
    };

    const resizeObserver = new ResizeObserver(resize);
    const intersectionObserver = new IntersectionObserver(([entry]) => {
        intersecting = entry?.isIntersecting ?? true;
        if (intersecting) start(); else stop();
    });
    const onVisibility = () => {
        visible = !document.hidden;
        if (visible) start(); else stop();
    };
    const onMotionChange = () => {
        stop();
        render();
        start();
    };
    const onContextLost = (event) => {
        event.preventDefault();
        contextLost = true;
        stop();
    };
    const onContextRestored = () => {
        contextLost = false;
        resize();
        start();
    };

    resizeObserver.observe(host);
    intersectionObserver.observe(host);
    document.addEventListener("visibilitychange", onVisibility);
    reducedMotion.addEventListener?.("change", onMotionChange);
    canvas.addEventListener("webglcontextlost", onContextLost);
    canvas.addEventListener("webglcontextrestored", onContextRestored);
    resize();
    start();

    window.addEventListener("pagehide", () => {
        stop();
        resizeObserver.disconnect();
        intersectionObserver.disconnect();
        document.removeEventListener("visibilitychange", onVisibility);
        reducedMotion.removeEventListener?.("change", onMotionChange);
        geometry.dispose();
        material.dispose();
        renderer.dispose();
    }, { once: true });
}

document.querySelectorAll("[data-structure-flow]").forEach(mountStructureFlow);
