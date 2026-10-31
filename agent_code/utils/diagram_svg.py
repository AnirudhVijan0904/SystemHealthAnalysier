import html
import os


def _severity_rank(sev):
    order = {"error": 3, "warn": 2, "warning": 2, "info": 1}
    return order.get((sev or "").lower(), 0)


def _node_colors(severity):
    sev = (severity or "").lower()
    if sev == "error":
        return "#fecaca", "#991b1b"
    if sev in {"warn", "warning"}:
        return "#fed7aa", "#9a3412"
    return "#dcfce7", "#166534"


def _edge_color(src_sev, tgt_sev):
    if _severity_rank(src_sev) >= 3 or _severity_rank(tgt_sev) >= 3:
        return "#dc2626"
    if _severity_rank(src_sev) >= 2 or _severity_rank(tgt_sev) >= 2:
        return "#ea580c"
    return "#16a34a"


def render_architecture_svg(
    servers,
    node_labels,
    edges,
    severity_map,
    output_path,
):
    col_w = 250
    node_w = 210
    node_h = 58
    header_h = 40
    pad = 24
    gap_x = 48
    gap_y = 14

    positions = {}
    cluster_boxes = []
    x = pad
    max_h = 0
    for server, nodes in servers.items():
        col_h = header_h + len(nodes) * (node_h + gap_y) + pad
        cluster_boxes.append((x, pad, col_w, col_h, server))
        y = pad + header_h
        for node_id in nodes:
            positions[node_id] = (x + 20, y, node_w, node_h)
            y += node_h + gap_y
        x += col_w + gap_x
        max_h = max(max_h, col_h)

    width = max(x + pad, 720)
    height = max_h + 110

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Segoe UI,Arial,sans-serif}</style>",
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<text x="24" y="18" font-size="14" font-weight="700" fill="#0f172a">System architecture and failing calls</text>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#334155"/></marker>',
        '<marker id="arrow-red" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#dc2626"/></marker>',
        '<marker id="arrow-orange" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#ea580c"/></marker>',
        '<marker id="arrow-green" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#16a34a"/></marker></defs>',
    ]

    for cx, cy, cw, ch, server in cluster_boxes:
        label = html.escape(str(server))
        parts.append(
            f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="#fff" stroke="#cbd5e1"/>'
        )
        parts.append(
            f'<text x="{cx + 12}" y="{cy + 24}" font-size="12" font-weight="700" fill="#334155">{label}</text>'
        )

    for node_id, (nx, ny, nw, nh) in positions.items():
        fill, stroke = _node_colors(severity_map.get(node_id))
        raw = node_labels.get(node_id, node_id).replace("\n", " · ")
        label = html.escape(raw)
        parts.append(
            f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="8" fill="{fill}" stroke="{stroke}"/>'
        )
        parts.append(
            f'<text x="{nx + nw / 2}" y="{ny + nh / 2 + 4}" text-anchor="middle" font-size="11" fill="#0f172a">{label}</text>'
        )

    for source, target in edges:
        if source not in positions or target not in positions:
            continue
        sx, sy, sw, sh = positions[source]
        tx, ty, tw, th = positions[target]
        x1, y1 = sx + sw, sy + sh / 2
        x2, y2 = tx, ty + th / 2
        color = _edge_color(severity_map.get(source), severity_map.get(target))
        marker = {
            "#dc2626": "url(#arrow-red)",
            "#ea580c": "url(#arrow-orange)",
            "#16a34a": "url(#arrow-green)",
        }.get(color, "url(#arrow)")
        mid_x = (x1 + x2) / 2
        parts.append(
            f'<path d="M{x1},{y1} C{mid_x},{y1} {mid_x},{y2} {x2},{y2}" fill="none" stroke="{color}" stroke-width="2.2" marker-end="{marker}"/>'
        )

    legend_y = height - 28
    parts.append(
        f'<circle cx="28" cy="{legend_y}" r="6" fill="#fecaca" stroke="#991b1b"/>'
        f'<text x="40" y="{legend_y + 4}" font-size="11" fill="#334155">Error / failed call</text>'
        f'<circle cx="180" cy="{legend_y}" r="6" fill="#fed7aa" stroke="#9a3412"/>'
        f'<text x="192" y="{legend_y + 4}" font-size="11" fill="#334155">Warning</text>'
        f'<circle cx="280" cy="{legend_y}" r="6" fill="#dcfce7" stroke="#166534"/>'
        f'<text x="292" y="{legend_y + 4}" font-size="11" fill="#334155">Healthy</text>'
    )
    parts.append("</svg>")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    return output_path
