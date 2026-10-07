import { useState } from 'react'
import {
  ArrowRight, BarChart3, ChartNoAxesColumnIncreasing, ChevronDown, CircleGauge,
  Cloud, Database, Droplets, Flame, Leaf, Lightbulb, Menu, Minus, Moon, Plus,
  Quote, Rocket, Sparkles, Sun, Target, TreePine, Weight, X, Zap,
} from 'lucide-react'
import './App.css'

const BIOMASS_TYPES = ['Rice Husk', 'Sugarcane Bagasse', 'Coconut Shell', 'Corn Stalk', 'Wood Waste', 'Food Waste']
const API_URL = 'http://127.0.0.1:5000'

function Navbar({ isDark, setIsDark }) {
  const [menuOpen, setMenuOpen] = useState(false)
  const links = [
    { label: 'Home', icon: Leaf, href: '#home' },
    { label: 'About', icon: Sparkles, href: '#about' },
    { label: 'How It Works', icon: CircleGauge, href: '#how-it-works' },
    { label: 'Impact (SDG)', icon: Target, href: '#impact' },
  ]
  return <nav className="navbar">
    <a className="brand" href="#home" aria-label="BioPredict home"><span className="brand-mark"><Leaf size={18} /></span><span><b>Bio</b><strong>Predict</strong></span></a>
    <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle navigation">{menuOpen ? <X size={20} /> : <Menu size={20} />}</button>
    <div className={`nav-links ${menuOpen ? 'open' : ''}`}>{links.map(({ label, icon: Icon, href }, index) => <a className={index === 0 ? 'active' : ''} href={href} key={label} onClick={() => setMenuOpen(false)}><Icon size={15} /> {label}</a>)}</div>
    <div className="nav-actions"><button className="icon-button" onClick={() => setIsDark(!isDark)} aria-label="Toggle theme">{isDark ? <Sun size={17} /> : <Moon size={17} />}</button><a className="deploy-button" href="#predict"><Rocket size={15} /> Deploy</a></div>
  </nav>
}

function FeatureHighlights() {
  const highlights = [{ icon: Zap, title: 'Fast', caption: 'Prediction' }, { icon: Target, title: 'Data-Driven', caption: 'Insights' }, { icon: Leaf, title: 'Supports', caption: 'Sustainability' }]
  return <div className="feature-highlights">{highlights.map(({ icon: Icon, title, caption }) => <div className="highlight" key={title}><span className="highlight-icon"><Icon size={18} /></span><span><b>{title}</b><small>{caption}</small></span></div>)}</div>
}

function QuoteCard() {
  return <article className="quote-card"><Quote className="quote-mark" size={78} /><div><p>“Turning organic waste into a<br />cleaner and brighter future.”</p><small>— Sustainable Energy for a Better Planet</small></div><Leaf className="quote-leaf" size={70} /></article>
}

function FeatureCards() {
  const cards = [{ icon: TreePine, title: <>Utilize<br />Agricultural Waste</>, text: <>Convert waste<br />into valuable energy</>, className: 'green' }, { icon: Cloud, title: <>Reduce<br />Carbon Footprint</>, text: <>Cleaner & greener<br />environment</>, className: 'blue' }, { icon: Lightbulb, title: <>Promote<br />Renewable Energy</>, text: <>Support the transition<br />to clean energy</>, className: 'gold' }, { icon: BarChart3, title: <>Aligns with<br />UN SDGs</>, text: <>Contribute to a<br />sustainable future</>, className: 'purple' }]
  return <div className="feature-cards" id="how-it-works">{cards.map(({ icon: Icon, title, text, className }) => <article className={`feature-card ${className}`} key={className}><Icon size={25} /><h3>{title}</h3><p>{text}</p></article>)}</div>
}

function HeroSection() {
  return <section className="hero-copy" id="about"><div className="hero-image-panel"><div className="hero-image-overlay" /><div className="hero-copy-content"><span className="eyebrow"><Leaf size={14} /> AI for a Greener Tomorrow</span><h1>Biomass<br /><em>Energy Predictor</em></h1><p>Estimate energy generation from user-provided<br className="desktop-only" /> biomass characteristics using Machine Learning.</p><FeatureHighlights /><QuoteCard /></div></div><FeatureCards /></section>
}

function NumberInput({ label, icon: Icon, value, setValue, unit, hint, step = 1, min = 0 }) {
  const adjust = (amount) => setValue(Math.max(min, Number((value + amount).toFixed(2))))
  return <label className="field"><span className="field-label"><Icon size={15} /> {label}</span><span className="input-shell"><input type="number" value={value.toFixed(2)} min={min} step={step} onChange={(event) => setValue(Number(event.target.value))} /><span className="stepper"><button type="button" onClick={() => adjust(-step)} aria-label={`Decrease ${label}`}><Minus size={13} /></button><button type="button" onClick={() => adjust(step)} aria-label={`Increase ${label}`}><Plus size={13} /></button></span><span className="unit">{unit}</span></span><small>{hint}</small></label>
}

function BiomassForm({ onPredict }) {
  const [biomassType, setBiomassType] = useState('Rice Husk')
  const [quantity, setQuantity] = useState(100)
  const [moisture, setMoisture] = useState(15)
  const [calorificValue, setCalorificValue] = useState(15)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const submit = async (event) => {
    event.preventDefault()
    if (quantity <= 0) return setError('Quantity must be greater than 0 kg.')
    if (moisture < 0 || moisture > 100) return setError('Moisture must be between 0 and 100%.')
    if (calorificValue <= 0) return setError('Calorific value must be greater than 0 MJ/kg.')
    setError(''); setIsLoading(true)
    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ biomass_type: biomassType, quantity_kg: quantity, moisture_percent: moisture, calorific_value_mj_kg: calorificValue }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Prediction request failed.')
      onPredict(data)
    } catch (requestError) {
      setError(`${requestError.message} Start the Python API with: python api.py`)
    } finally {
      setIsLoading(false)
    }
  }
  return <section className="form-card" id="predict"><div className="card-heading"><span className="heading-icon"><Leaf size={18} /></span><div><h2>Enter Biomass Information</h2><p>Provide the characteristics of your biomass to predict the potential energy generation.</p></div></div><div className="divider" /><form onSubmit={submit}><label className="field"><span className="field-label"><Database size={15} /> Biomass Type</span><span className="select-shell"><select value={biomassType} onChange={(event) => setBiomassType(event.target.value)}>{BIOMASS_TYPES.map((type) => <option key={type}>{type}</option>)}</select><ChevronDown size={16} /></span></label><NumberInput label="Quantity of Biomass (kg)" icon={Weight} value={quantity} setValue={setQuantity} unit="kg" hint="Amount of biomass available" /><NumberInput label="Moisture Percentage (%)" icon={Droplets} value={moisture} setValue={setMoisture} unit="%" hint="Moisture content in the biomass" step={0.5} /><NumberInput label="Calorific Value (MJ/kg)" icon={Flame} value={calorificValue} setValue={setCalorificValue} unit="MJ/kg" hint="Energy content per kg of biomass" step={0.5} />{error && <p className="form-error">{error}</p>}<button className="predict-button" type="submit" disabled={isLoading}><ChartNoAxesColumnIncreasing size={18} /> {isLoading ? 'Connecting to ML model...' : 'Predict Energy Output'} <ArrowRight size={18} /></button></form></section>
}

function PredictionResult({ result }) {
  return <section className={`result-card ${result ? 'has-result' : ''}`}><div className="card-heading"><span className="heading-icon"><Zap size={18} /></span><div><h2>Prediction Result</h2><p>{result ? 'Your ML-based estimate is ready.' : 'Your estimated energy output will appear here.'}</p></div></div><div className="result-body"><div className="result-copy">{result ? <><span className="result-label">Predicted Energy Generation</span><strong>{result.prediction.toFixed(2)} <small>kWh</small></strong><span className="co2-value">Estimated CO₂ Reduction <b>{result.co2.toFixed(2)} kg CO₂</b></span></> : <><span className="empty-result-icon"><Lightbulb size={28} /></span><h3>No prediction yet</h3><p>Fill in the details and click on<br /><b>“Predict Energy Output”</b> to see the results.</p></>}</div><div className="result-art"><Lightbulb size={62} /><Leaf size={32} /></div></div></section>
}

function SDGSection() {
  const sdgs = [{ number: '7', title: 'Affordable and Clean Energy', className: 'sdg-yellow' }, { number: '12', title: 'Responsible Consumption and Production', className: 'sdg-orange' }, { number: '13', title: 'Climate Action', className: 'sdg-green' }]
  return <section className="sdg-section" id="impact"><div><span className="section-kicker">Our positive footprint</span><h2>Sustainable Development Goals</h2><div className="sdg-cards">{sdgs.map(({ number, title, className }) => <article className={`sdg-card ${className}`} key={number}><strong>SDG<br /><b>{number}</b></strong><span>{title}</span></article>)}</div></div><div className="big-change"><Leaf size={25} /><span>Small biomass.<br /><b>Big change.</b></span></div></section>
}

function Footer() { return <footer><span><Leaf size={14} /> BioPredict</span><small>Software-only ML estimates for a greener tomorrow.</small><span className="offline"><span /> No hardware required</span></footer> }

function App() {
  const [isDark, setIsDark] = useState(true)
  const [result, setResult] = useState(null)
  const predict = (data) => setResult({ ...data, prediction: data.predicted_energy_kwh, co2: data.estimated_co2_reduction_kg })
  return <div className={`app-shell ${isDark ? 'dark' : 'light'}`}><Navbar isDark={isDark} setIsDark={setIsDark} /><main><HeroSection /><div className="workspace-grid"><BiomassForm onPredict={predict} /><PredictionResult result={result} /></div><SDGSection /></main><Footer /></div>
}

export default App
