import React, { Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stage, useGLTF } from '@react-three/drei'

function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url)
  return <primitive object={scene} />
}

export const Outfit3DViewer: React.FC<{ modelUrl: string; className?: string }> = ({ modelUrl, className }) => {
  return (
    <div className={className ?? 'w-full h-96 bg-black/5 rounded'}>
      <Canvas camera={{ position: [1.5, 1.5, 1.5], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <Suspense fallback={null}>
          <Stage intensity={0.6} environment={null}>
            <Model url={modelUrl} />
          </Stage>
        </Suspense>
        <OrbitControls enablePan enableZoom enableRotate />
      </Canvas>
    </div>
  )
}

useGLTF.preload('/placeholder.glb')

