import { NavLink } from "react-router-dom";
import { BrainCircuit } from "lucide-react";
import { NAV_ITEMS } from "../../utils/constants";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-brand">
        <div className="brand-icon">
          <BrainCircuit size={22} />
        </div>

        <div>
          <h1>TalentMosaic</h1>
          <p>Segmentación inteligente de freelancers y reseñas</p>
        </div>
      </div>

      <nav className="navbar-links">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              isActive ? "nav-link nav-link-active" : "nav-link"
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}

export default Navbar;