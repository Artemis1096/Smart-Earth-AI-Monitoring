import React, { useRef } from 'react';
import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import * as THREE from 'three';

function Earth() {
  const earthRef = useRef();

  const texture = useLoader(THREE.TextureLoader, 'earthmap.jpg');

  useFrame(() => {
    if (earthRef.current) {
      earthRef.current.rotation.y += 0.002;
    }
  });

  return (
    <mesh ref={earthRef}>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial map={texture} />
    </mesh>
  );
}

export default function RevolvingEarth() {
  return (
    <div style={{ width: '100%', height: '60vh', background: 'black' }}>
      <Canvas camera={{ position: [0, 0, 3] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[5, 5, 5]} intensity={1.2} />
        <OrbitControls enableZoom={true} />
        <Stars radius={100} depth={50} count={5000} factor={6} fade />
        <Earth />
      </Canvas>
    </div>
  );
}
