import { useEffect, useState } from 'react'

type Health = Record<string, unknown>
type Order = { item: string; qty: number; createdAt: string }

const WEB_SHA = import.meta.env.VITE_GIT_SHA ?? 'dev'

export default function App() {
  const [orders, setOrders] = useState<Order[]>([])
  const [count, setCount] = useState('0')
  const [item, setItem] = useState('')
  const [health, setHealth] = useState<Record<string, Health | string>>({})
  const [question, setQuestion] = useState('Say hi in five words.')
  const [reply, setReply] = useState('')

  const load = async () => {
    const r = await fetch('/api/orders')
    const j = await r.json()
    setOrders(j.orders)
    setCount(j.count)
  }

  useEffect(() => {
    load()
    for (const s of ['orders', 'chat']) {
      fetch(`/api/${s}/healthz`)
        .then((r) => r.json())
        .then((j) => setHealth((h) => ({ ...h, [s]: j })))
        .catch((e) => setHealth((h) => ({ ...h, [s]: String(e) })))
    }
  }, [])

  const add = async () => {
    if (!item) return
    await fetch('/api/orders', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ item, qty: 1 }),
    })
    setItem('')
    load()
  }

  const ask = async () => {
    setReply('…')
    const r = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ message: question }),
    })
    const j = await r.json()
    setReply(r.ok ? j.reply : `error: ${j.detail}`)
  }

  return (
    <main style={{ fontFamily: 'system-ui', maxWidth: 640, margin: '2rem auto', lineHeight: 1.5 }}>
      <h1>pilot-monorepo</h1>
      <p>
        web sha <code>{WEB_SHA}</code> · host <code>{location.host}</code>
      </p>
      <h2>Health</h2>
      <pre>{JSON.stringify(health, null, 2)}</pre>

      <h2>Orders ({count} created)</h2>
      <input value={item} onChange={(e) => setItem(e.target.value)} placeholder="item" />
      <button onClick={add}>add</button>
      <ul>
        {orders.map((o) => (
          <li key={o.createdAt}>
            {o.item} × {o.qty} <small>{o.createdAt}</small>
          </li>
        ))}
      </ul>

      <h2>Chat (OpenRouter)</h2>
      <input value={question} onChange={(e) => setQuestion(e.target.value)} style={{ width: '70%' }} />
      <button onClick={ask}>ask</button>
      <p>{reply}</p>
    </main>
  )
}
