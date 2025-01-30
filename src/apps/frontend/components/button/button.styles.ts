const styles = {
  kind: {
    primary: {
      base: `
        active:bg-primary/80
        bg-primary
        border
        flex
        font-medium
        items-center
        justify-center
        p-4
        rounded-lg
        text-white
        transition
        w-full
      `,
      disableState: 'cursor-not-allowed bg-primary/80',
      enableState: 'hover:bg-primary/90 cursor-pointer',
    },
    secondary: {
      base: `
        inset-y-0
        flex
        items-center
      `,
      disableState: 'cursor-not-allowed',
      enableState: 'cursor-pointer',
    },
    tertiary: {
      base: `
        active:bg-transparent
        bg-transparent
        text-primary
        text-lg
        text-center
      `,
      disableState: 'cursor-not-allowed text-slate-500',
      enableState: 'cursor-pointer',
    },
    danger: {
      base: `
        active:bg-danger/80
        bg-danger
        border
        flex
        font-medium
        gap-2
        items-center
        justify-center
        px-4
        rounded-md
        text-white
        transition
        w-full
      `,
      disableState: 'cursor-not-allowed bg-danger/80',
      enableState: 'hover:bg-danger/90 cursor-pointer',
    },
  },
  size: {
    compact: 'p-2',
    default: 'p-2.5',
    large: 'p-3.5',
    mini: 'p-1.5',
  },
};

export default styles;
