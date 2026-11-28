import React from "react";
import SelectComponent from "react-select";
import CreatableSelect from "react-select/creatable";
import type {
  ActionMeta,
  Props as ReactSelectProps,
  SingleValue,
  StylesConfig,
} from "react-select";

export type SelectOption = {
  value: string;
  label: string;
  isDisabled?: boolean;
};

type BaseProps = {
  value: string | null;
  options: SelectOption[];
  placeholder?: string;
  disabled?: boolean;
  isLoading?: boolean;
  isClearable?: boolean;
  onChange: (value: string | null, action: ActionMeta<SelectOption>) => void;
  onBlur?: () => void;
  className?: string;
  formatCreateLabel?: (input: string) => string;
};

type CreatableProps = {
  isCreatable: true;
  onCreateOption: (value: string) => void;
};

type NonCreatableProps = {
  isCreatable?: false;
  onCreateOption?: never;
};

export type SelectProps = BaseProps & (CreatableProps | NonCreatableProps);

const baseBackground = "var(--color-control)";
const hoverBackground = "var(--color-hover)";
const neutralBorder = "var(--color-edge)";

const selectStyles: StylesConfig<SelectOption, false> = {
  control: (base, state) => ({
    ...base,
    minHeight: 30,
    borderRadius: 6,
    borderColor: state.isFocused ? "var(--color-accent)" : neutralBorder,
    boxShadow: state.isFocused ? "0 0 0 1px var(--color-accent)" : "none",
    backgroundColor: baseBackground,
    fontSize: "13px",
    fontWeight: 500,
    color: "var(--color-text)",
    transition: "border-color 120ms ease, box-shadow 120ms ease",
    ":hover": {
      borderColor: state.isFocused
        ? "var(--color-accent)"
        : "var(--color-edge-strong)",
    },
  }),
  valueContainer: (base) => ({
    ...base,
    paddingInline: 8,
    paddingBlock: 0,
  }),
  input: (base) => ({
    ...base,
    color: "var(--color-text)",
  }),
  singleValue: (base) => ({
    ...base,
    color: "var(--color-text)",
  }),
  dropdownIndicator: (base, state) => ({
    ...base,
    color: "var(--color-ink-3)",
    padding: 4,
    ":hover": {
      color: "var(--color-text)",
    },
  }),
  clearIndicator: (base) => ({
    ...base,
    color: "var(--color-ink-3)",
    ":hover": {
      color: "var(--color-logo-primary)",
    },
  }),
  menu: (provided) => ({
    ...provided,
    zIndex: 30,
    backgroundColor: "var(--color-menu)",
    color: "var(--color-text)",
    border: "1px solid var(--color-edge)",
    borderRadius: 8,
    boxShadow: "0 8px 24px rgba(0, 0, 0, 0.45)",
    overflow: "hidden",
    fontSize: "13px",
  }),
  option: (base, state) => ({
    ...base,
    backgroundColor: state.isSelected
      ? "var(--color-control)"
      : state.isFocused
        ? hoverBackground
        : "transparent",
    color: state.isSelected ? "var(--color-emphasis)" : "var(--color-text)",
    fontSize: "13px",
    fontWeight: 500,
    cursor: state.isDisabled ? "not-allowed" : base.cursor,
    opacity: state.isDisabled ? 0.5 : 1,
  }),
  placeholder: (base) => ({
    ...base,
    color: "var(--color-ink-3)",
  }),
};

export const Select: React.FC<SelectProps> = React.memo(
  ({
    value,
    options,
    placeholder,
    disabled,
    isLoading,
    isClearable = true,
    onChange,
    onBlur,
    className = "",
    isCreatable,
    formatCreateLabel,
    onCreateOption,
  }) => {
    const selectValue = React.useMemo(() => {
      if (!value) return null;
      const existing = options.find((option) => option.value === value);
      if (existing) return existing;
      return { value, label: value, isDisabled: false };
    }, [value, options]);

    const handleChange = (
      option: SingleValue<SelectOption>,
      action: ActionMeta<SelectOption>,
    ) => {
      onChange(option?.value ?? null, action);
    };

    const sharedProps: Partial<ReactSelectProps<SelectOption, false>> = {
      className,
      classNamePrefix: "app-select",
      value: selectValue,
      options,
      onChange: handleChange,
      placeholder,
      isDisabled: disabled,
      isLoading,
      onBlur,
      isClearable,
      styles: selectStyles,
    };

    if (isCreatable) {
      return (
        <CreatableSelect<SelectOption, false>
          {...sharedProps}
          onCreateOption={onCreateOption}
          formatCreateLabel={formatCreateLabel}
        />
      );
    }

    return <SelectComponent<SelectOption, false> {...sharedProps} />;
  },
);

Select.displayName = "Select";
