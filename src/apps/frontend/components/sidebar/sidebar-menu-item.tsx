import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';

type SidebarMenuItemProps = {
  iconPath: string;
  path: string;
  setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>;
  subItems?: { path: string; title: string }[];
  title: string;
};

const SidebarMenuItem: React.FC<SidebarMenuItemProps> = ({
  iconPath,
  path,
  setIsSidebarOpen,
  subItems,
  title,
}) => {
  const location = useLocation();
  const { pathname } = location;
  const [open, setOpen] = useState<boolean>(pathname.includes(path));

  const handleOpen = () => {
    setOpen(!open);
  };

  return (
    <li>
      <NavLink
        to={subItems ? '#' : path}
        className={`group relative flex items-center gap-2.5 rounded-sm px-4 py-2 font-medium text-bodydark1 duration-300 ease-in-out hover:bg-graydark dark:hover:bg-meta-4 ${
          (pathname === path || pathname.includes(title.toLowerCase())) &&
          'bg-graydark dark:bg-meta-4'
        }`}
        onClick={() => {
          if (subItems) {
            handleOpen();
            return;
          }
          setIsSidebarOpen(false);
        }}
      >
        <img src={iconPath} alt={`${title} icon`} />
        {title}
        {subItems && (
          <img
            src={
              open
                ? '/assets/img/icon/chevron-up-solid.svg'
                : '/assets/img/icon/chevron-down-solid.svg'
            }
            alt="chevron icon"
            className="absolute right-4"
          />
        )}
      </NavLink>
      {subItems && open && (
        <div className="max-h-40 overflow-hidden duration-300 ease-in-out">
          <ul className="mb-5 mt-3.5 flex flex-col gap-2.5 pl-6">
            {subItems.map((subItem) => (
              <li key={subItem.path}>
                <NavLink
                  to={subItem.path}
                  className={({ isActive }) =>
                    `group relative flex items-center gap-2.5 rounded-md px-4 font-medium text-bodydark2 duration-300 ease-in-out hover:text-white ${
                      isActive && '!text-white'
                    }`
                  }
                  onClick={() => setIsSidebarOpen(false)}
                >
                  {subItem.title}
                </NavLink>
              </li>
            ))}
          </ul>
        </div>
      )}
    </li>
  );
};

export default SidebarMenuItem;
