import { Collection, CheckboxField, Flex } from '@aws-amplify/ui-react';
import { FaTrashAlt } from 'react-icons/fa';

export default function ListLi({ items, handleCheck, handleDelete }) {
  return (
    <Collection
      items={items}
      wrap="nowrap"
    >
      {(item) => (
        <li
          key={item.id}
          className="no-bullet"
        >
          <Flex
            direction="row"
            justifyContent="flex-start"
            alignItems="stretch"
            alignContent="flex-start"
            wrap="nowrap"
            gap="1rem"
          >
            <CheckboxField
              name={item.id}
              checked={item.checked}
              onChange={(() => handleCheck(item.id))}
            />
            <label
              htmlFor="normal"
              onDoubleClick={() => handleCheck(item.id)}
              style={(item.checked) ? { textDecoration: "line-through" } : null}
            >{item.item}</label>
  
            <FaTrashAlt
              onClick={() => handleDelete(item.id)}
              role="button"
              tabIndex="0"
              stoke="#9580ff"
              fill="#808080" 
              aria-label={`Delete ${item.item}`}
            />
          </Flex>
        </li>
      )}
    </Collection>
  );
}