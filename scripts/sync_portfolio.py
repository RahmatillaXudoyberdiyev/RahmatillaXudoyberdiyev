import os
import re
import sys
import json
import urllib.request
import urllib.error

API_URL = "https://www.rahmatilla.uz/api/portfolio"
BASE_URL = "https://www.rahmatilla.uz"

BADGE_MAP = {
    "Agentic AI Workflows": "https://img.shields.io/badge/Agentic_AI-Multi--Agent_Orchestration-blueviolet?style=flat-square",
    "Multi-Agent Orchestration": "https://img.shields.io/badge/Orchestration-Multi--Agent-8A2BE2?style=flat-square",
    "Reflection & Self-Correction": "https://img.shields.io/badge/Reflection-Self--Correction-4B0082?style=flat-square",
    "Tool Use & Function Calling": "https://img.shields.io/badge/Tools-Function_Calling-6A0DAD?style=flat-square",
    "Task Planning & Decomposition": "https://img.shields.io/badge/Planning-Decomposition-7B1FA2?style=flat-square",
    "Multi-LLM Routing (Gemini & Groq & Cloudflare)": "https://img.shields.io/badge/LLM_Routing-Gemini_|_Groq_|_Cloudflare-orange?style=flat-square",
    "Multi-LLM Routing": "https://img.shields.io/badge/LLM_Routing-Gemini_|_Groq_|_Cloudflare-orange?style=flat-square",
    "Local-First Architecture": "https://img.shields.io/badge/Architecture-Local--First-00897B?style=flat-square",
    "WebAssembly Sandboxing": "https://img.shields.io/badge/Sandbox-WebAssembly_WASM-654FF0?style=flat-square&logo=webassembly&logoColor=white",
    "Python": "https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white",
    "Django": "https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white",
    "Flask": "https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white",
    "Next.js": "https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white",
    "React": "https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB",
    "Nest.js": "https://img.shields.io/badge/Nest.js-E0234E?style=flat-square&logo=nestjs&logoColor=white",
    "PostgreSQL": "https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white",
    "MySQL": "https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white",
    "SQLAlchemy": "https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white",
    "SQL": "https://img.shields.io/badge/SQL-336791?style=flat-square&logo=postgresql&logoColor=white",
    "TensorFlow": "https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white",
    "Tensorflow": "https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white",
    "Keras": "https://img.shields.io/badge/Keras-D00000?style=flat-square&logo=keras&logoColor=white",
    "OpenCV": "https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white",
    "Scikit-Learn": "https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white",
    "spaCy": "https://img.shields.io/badge/spaCy-09A3D5?style=flat-square&logo=spacy&logoColor=white",
    "NumPy": "https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white",
    "Pandas": "https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white",
    "Dask": "https://img.shields.io/badge/Dask-FD5A1E?style=flat-square&logo=dask&logoColor=white",
    "Matplotlib": "https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logo=python&logoColor=white",
    "Seaborn": "https://img.shields.io/badge/Seaborn-388E3C?style=flat-square",
    "Scrapy": "https://img.shields.io/badge/Scrapy-5A29E4?style=flat-square&logo=scrapy&logoColor=white",
    "Aiogram": "https://img.shields.io/badge/Aiogram-2CA5E0?style=flat-square&logo=telegram&logoColor=white",
    "PyQt6": "https://img.shields.io/badge/PyQt6-41CD52?style=flat-square&logo=qt&logoColor=white",
    "Git": "https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white",
    "GitHub": "https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white",
    "LangChain": "https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white",
    "Image Segmentation": "https://img.shields.io/badge/Computer_Vision-Image_Segmentation-5C3EE8?style=flat-square",
    "Retrieval-Augmented Generation (RAG)": "https://img.shields.io/badge/AI-RAG-blueviolet?style=flat-square",
    "LlamaIndex": "https://img.shields.io/badge/LlamaIndex-1C3C3C?style=flat-square",
    "Gradio": "https://img.shields.io/badge/Gradio-FF7C00?style=flat-square",
    "IBM Watson": "https://img.shields.io/badge/IBM_Watson-052FAD?style=flat-square&logo=ibm&logoColor=white",
    "Kerio Control": "https://img.shields.io/badge/Security-Kerio_Control-0072C6?style=flat-square",
    "Hikvision": "https://img.shields.io/badge/Security-Hikvision-D32F2F?style=flat-square"
}

def sanitize_slug(name):
    clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', name.lower().strip())
    return re.sub(r'_+', '_', clean).strip('_')

def get_badge(skill):
    if skill in BADGE_MAP:
        return f"![{skill}]({BADGE_MAP[skill]})"
    safe = re.sub(r'[^a-zA-Z0-9]', '_', skill)
    return f"![{skill}](https://img.shields.io/badge/{safe}-374151?style=flat-square)"

def fetch_portfolio_data():
    try:
        print(f"Requesting data from {API_URL}...")
        req = urllib.request.Request(API_URL, headers={"User-Agent": "GitHub-Profile-Sync/1.0"})
        with urllib.request.urlopen(req, timeout=15) as res:
            content = res.read().decode("utf-8")
            data = json.loads(content)
            print("Successfully received and parsed portfolio data.")
            return data
    except Exception as e:
        print(f"Error fetching portfolio data: {e}", file=sys.stderr)
        raise

def download_preview_image(image_relative_url, project_title, target_dir):
    try:
        os.makedirs(target_dir, exist_ok=True)
        slug = sanitize_slug(project_title)
        local_filename = f"{slug}.png"
        local_path = os.path.join(target_dir, local_filename)
        repo_relative_path = f"assets/{local_filename}"

        full_url = f"{BASE_URL}{image_relative_url}" if image_relative_url.startswith("/") else image_relative_url
        print(f"Downloading preview for '{project_title}' from {full_url}...")
        req = urllib.request.Request(full_url, headers={"User-Agent": "GitHub-Profile-Sync/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(local_path, "wb") as f:
                f.write(response.read())
        print(f"Saved preview image to {local_path}.")
        try:
            from PIL import Image
            with Image.open(local_path) as im:
                if im.width > 1000:
                    ratio = 1000.0 / float(im.width)
                    new_height = int(float(im.height) * ratio)
                    im_resized = im.resize((1000, new_height), Image.Resampling.LANCZOS)
                    im_resized.save(local_path, "PNG", optimize=True)
                    print(f"Optimized image for '{project_title}' to 1000x{new_height}.")
        except Exception as resize_err:
            print(f"Image resize skipped: {resize_err}")
        return repo_relative_path
    except Exception as e:
        print(f"Failed to download image for '{project_title}': {e}. Using remote URL.", file=sys.stderr)
        return f"{BASE_URL}{image_relative_url}" if image_relative_url.startswith("/") else image_relative_url

def generate_header(profile):
    name = profile.get("name", "Rahmatilla Xudoyberdiyev")
    location = profile.get("location", "Tashkent, Uzbekistan")
    status = profile.get("status", "Available for new projects")
    telegram = profile.get("telegram", "https://t.me/rahmatilla_uz")
    linkedin = profile.get("linkedin", "https://www.linkedin.com/in/rahmatilla-xudoyberdiyev")
    email = profile.get("email", "xudoyberdiyevrahmatilla@gmail.com")
    resume_url = profile.get("resumeUrl", "/resume.pdf")
    if resume_url.startswith("/"):
        resume_url = f"{BASE_URL}{resume_url}"

    lines = [
        '<div align="center">',
        "",
        f"# Hi there, I'm {name} 👋",
        "### AI Systems & Agentic Workflows Engineer",
        "",
        "[![GitHub Streak](https://streak-stats.demolab.com/?user=RahmatillaXudoyberdiyev&theme=dark)](https://git.io/streak-stats)",
        "",
        f"📍 **{location}** | 💼 **{status}**  ",
        f"🌐 [rahmatilla.uz]({BASE_URL}) • 💬 [Telegram]({telegram}) • 💼 [LinkedIn]({linkedin}) • ✉️ [Email](mailto:{email}) • 📄 [Resume / CV]({resume_url})",
        "",
        "</div>",
        "",
        "---",
        "",
        "### 🚀 About Me",
        ""
    ]
    for paragraph in profile.get("aboutParagraphs", []):
        lines.append(f"{paragraph}\n")
    lines.append("---")
    return "\n".join(lines)

def generate_projects(projects, assets_dir):
    lines = [
        "### 🌟 Featured Projects",
        ""
    ]
    sorted_projects = sorted(projects, key=lambda x: (not x.get("pinned", False)))
    featured_projects = sorted_projects[:3]
    remaining_projects = sorted_projects[3:]

    for proj in featured_projects:
        title = proj.get("title", "").strip()
        link = proj.get("link", "").strip()
        proj_type = proj.get("type", "").strip()
        status = proj.get("status", "").strip()
        status_badge = f" `{status}`" if status else ""
        type_str = f" — {proj_type}" if proj_type else ""

        if link:
            lines.append(f"#### 🤖 [{title}]({link}){type_str}{status_badge}")
        else:
            lines.append(f"#### 🤖 {title}{type_str}{status_badge}")

        bullet_points = proj.get("bulletPoints", [])
        for bp in bullet_points:
            lines.append(f"* {bp}")

        skills = proj.get("skills", [])
        if skills:
            badge_list = [get_badge(s) for s in skills]
            lines.append("")
            lines.append(" ".join(badge_list))

        preview_img = proj.get("previewImageUrl", "")
        if preview_img:
            image_src = download_preview_image(preview_img, title, assets_dir)
            lines.append("")
            if link:
                lines.append(f'<p align="center"><a href="{link}"><img src="{image_src}" alt="{title}" width="520" /></a></p>')
            else:
                lines.append(f'<p align="center"><img src="{image_src}" alt="{title}" width="520" /></p>')
        lines.append("")

    if remaining_projects:
        lines.append("<details>")
        lines.append(f"<summary><b>📂 More Projects ({len(remaining_projects)})</b></summary>")
        lines.append("")
        lines.append("| Project | Type | Tech Stack | Link |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for proj in remaining_projects:
            title = proj.get("title", "").strip()
            link = proj.get("link", "").strip()
            proj_type = proj.get("type", "Project").strip()
            skills_str = ", ".join(proj.get("skills", []))
            link_md = f"[Open ↗]({link})" if link else "—"
            lines.append(f"| **{title}** | {proj_type} | {skills_str} | {link_md} |")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    lines.append("---")
    return "\n".join(lines)

def generate_skills(skills_data):
    lines = [
        "### 🛠️ Tech Stack & Skills",
        ""
    ]
    featured_skills = skills_data[:3]
    remaining_skills = skills_data[3:]

    for cat in featured_skills:
        cat_name = cat.get("name", "")
        lines.append(f"**{cat_name}**  ")
        badges = [get_badge(tech) for tech in cat.get("technologies", [])]
        lines.append(" ".join(badges))
        lines.append("")

    if remaining_skills:
        lines.append("<details>")
        lines.append(f"<summary><b>🧩 Additional Skills & Tooling ({len(remaining_skills)} categories)</b></summary>")
        lines.append("")
        for cat in remaining_skills:
            cat_name = cat.get("name", "")
            lines.append(f"**{cat_name}**  ")
            badges = [get_badge(tech) for tech in cat.get("technologies", [])]
            lines.append(" ".join(badges))
            lines.append("")
        lines.append("</details>")
        lines.append("")

    lines.append("---")
    return "\n".join(lines)

def generate_experience(experience_data):
    lines = [
        "### 💼 Experience",
        ""
    ]
    featured_exp = experience_data[:3]
    remaining_exp = experience_data[3:]

    for exp in featured_exp:
        role = exp.get("profession", "").strip()
        company = exp.get("company", "").strip()
        period = exp.get("period", "").strip()
        location = exp.get("location", "").strip()
        work_type = exp.get("workType", "").strip()
        subtext = " · ".join(filter(None, [period, work_type, location]))

        lines.append(f"#### 🏢 {role} — **{company}**")
        if subtext:
            lines.append(f"_{subtext}_  ")
        for bp in exp.get("bulletPoints", []):
            lines.append(f"* {bp}")
        skills = exp.get("skills", [])
        if skills:
            lines.append("`" + "` `".join(skills) + "`")
        lines.append("")

    if remaining_exp:
        lines.append("<details>")
        lines.append(f"<summary><b>💼 View Earlier Experience ({len(remaining_exp)})</b></summary>")
        lines.append("")
        for exp in remaining_exp:
            role = exp.get("profession", "").strip()
            company = exp.get("company", "").strip()
            period = exp.get("period", "").strip()
            lines.append(f"* **{role}** at **{company}** ({period})")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    lines.append("---")
    return "\n".join(lines)

def generate_certificates(cert_data):
    lines = [
        "### 📜 Verified Credentials & Certifications",
        ""
    ]
    featured_certs = cert_data[:3]
    remaining_certs = cert_data[3:]

    for cert in featured_certs:
        name = cert.get("name", "").strip()
        provider = cert.get("provider", "").strip()
        issued = cert.get("issuedDate", "").strip()
        cred_url = cert.get("credentialUrl", "").strip()
        pdf_url = cert.get("pdfUrl", "").strip()

        target_url = cred_url
        if not target_url and pdf_url:
            target_url = f"{BASE_URL}{pdf_url}" if pdf_url.startswith("/") else pdf_url

        date_str = f" ({issued})" if issued else ""
        if target_url:
            lines.append(f"* **[{name}]({target_url})** — {provider}{date_str}")
        else:
            lines.append(f"* **{name}** — {provider}{date_str}")

    if remaining_certs:
        lines.append("")
        lines.append("<details>")
        lines.append(f"<summary><b>📜 More Certifications ({len(remaining_certs)})</b></summary>")
        lines.append("")
        for cert in remaining_certs:
            name = cert.get("name", "").strip()
            provider = cert.get("provider", "").strip()
            issued = cert.get("issuedDate", "").strip()
            cred_url = cert.get("credentialUrl", "").strip()
            pdf_url = cert.get("pdfUrl", "").strip()
            target_url = cred_url
            if not target_url and pdf_url:
                target_url = f"{BASE_URL}{pdf_url}" if pdf_url.startswith("/") else pdf_url
            date_str = f" ({issued})" if issued else ""
            if target_url:
                lines.append(f"* [{name}]({target_url}) — {provider}{date_str}")
            else:
                lines.append(f"* {name} — {provider}{date_str}")
        lines.append("")
        lines.append("</details>")

    lines.append("")
    lines.append("---")
    return "\n".join(lines)

def generate_education(education_data):
    lines = [
        "### 🎓 Education",
        ""
    ]
    featured_edu = education_data[:3]
    remaining_edu = education_data[3:]

    for edu in featured_edu:
        degree = edu.get("degree", "").strip()
        institution = edu.get("institution", "").strip()
        period = edu.get("period", "").strip()
        description = edu.get("description", "").strip()

        lines.append(f"#### 🏛️ {institution}")
        lines.append(f"**{degree}** | _{period}_  ")
        if description:
            lines.append(f"{description}  ")
        skills = edu.get("skills", [])
        if skills:
            lines.append("`" + "` `".join(skills) + "`")
        lines.append("")

    if remaining_edu:
        lines.append("<details>")
        lines.append(f"<summary><b>🎓 View Prior Education ({len(remaining_edu)})</b></summary>")
        lines.append("")
        for edu in remaining_edu:
            degree = edu.get("degree", "").strip()
            institution = edu.get("institution", "").strip()
            period = edu.get("period", "").strip()
            lines.append(f"* **{degree}** — {institution} ({period})")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    lines.append("---")
    return "\n".join(lines)

def generate_languages(languages_data):
    lines = [
        "### 🌐 Languages",
        ""
    ]
    featured_langs = languages_data[:3]
    remaining_langs = languages_data[3:]

    lang_items = []
    for lang in featured_langs:
        l_name = lang.get("language", "").strip()
        l_level = lang.get("level", "").strip()
        lang_items.append(f"**{l_name}**: `{l_level}`")
    lines.append(" • ".join(lang_items))

    if remaining_langs:
        more_items = []
        for lang in remaining_langs:
            l_name = lang.get("language", "").strip()
            l_level = lang.get("level", "").strip()
            more_items.append(f"{l_name}: `{l_level}`")
        lines.append("")
        lines.append("<details>")
        lines.append(f"<summary><b>More Languages ({len(remaining_langs)})</b></summary>")
        lines.append("")
        lines.append(" • ".join(more_items))
        lines.append("")
        lines.append("</details>")

    lines.append("")
    lines.append("---")
    return "\n".join(lines)

def generate_footer(profile):
    telegram = profile.get("telegram", "https://t.me/rahmatilla_uz")
    linkedin = profile.get("linkedin", "https://www.linkedin.com/in/rahmatilla-xudoyberdiyev")
    lines = [
        '<div align="center">',
        f'  <sub>Let\'s connect: <a href="{telegram}">Telegram</a> • <a href="{linkedin}">LinkedIn</a> • <a href="{BASE_URL}">rahmatilla.uz</a></sub>',
        "</div>"
    ]
    return "\n".join(lines)

def main():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme_path = os.path.join(base_dir, "README.md")
        assets_dir = os.path.join(base_dir, "assets")

        data = fetch_portfolio_data()

        profile_sec = generate_header(data.get("profile", {}))
        projects_sec = generate_projects(data.get("projects", []), assets_dir)
        skills_sec = generate_skills(data.get("skills", []))
        exp_sec = generate_experience(data.get("experience", []))
        certs_sec = generate_certificates(data.get("certificates", []))
        edu_sec = generate_education(data.get("education", []))
        lang_sec = generate_languages(data.get("languages", []))
        footer_sec = generate_footer(data.get("profile", {}))

        full_content = "\n\n".join([
            profile_sec,
            projects_sec,
            skills_sec,
            exp_sec,
            certs_sec,
            edu_sec,
            lang_sec,
            footer_sec
        ]) + "\n"

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        print(f"Successfully generated dynamic README at {readme_path}")
    except Exception as e:
        print(f"Error during synchronization: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
