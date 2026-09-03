import { useState } from "react";

export default function ImageUpload({ onSelect }) {
  const [preview, setPreview] = useState(null);
  const handle = e => {
    const file = e.target.files?.[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    onSelect(file);
  };
  return (
    <div className="upload-card">
      <label className="upload-box">
        <input type="file" accept="image/*" onChange={handle} hidden />
        <span>📷 Choose a waste image</span>
        <small>JPG, PNG or WebP</small>
      </label>
      {preview && <img className="preview" src={preview} alt="Selected waste" />}
    </div>
  );
}
